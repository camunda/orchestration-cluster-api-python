"""Backpressure must travel from a real HTTP response all the way to the gate.

``tests/acceptance/test_backpressure.py`` covers the two halves in isolation:
``is_backpressure_response`` with bare integers, and the manager driven by direct
``record_backpressure()`` / ``acquire()`` calls. Neither exercises the wiring between
them, which the post-gen hook emits into every generated client method. A hook change
that dropped ``record_backpressure()`` from a branch, misclassified an error type, or
moved a method in or out of the bypass set would leave all of those tests green.

So these drive real responses through a real client over an ``httpx.MockTransport``
and assert the resulting gating, and a class-scoped check asserts that every generated
API method routes through ``_bp`` except exactly the bypass set.
"""

from __future__ import annotations

import inspect
import threading
from typing import Any, Callable, cast

import httpx
import pytest

from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient, errors
from camunda_orchestration_sdk.runtime.backpressure import (
    EXEMPT_METHODS,
    BackpressureManager,
)
from camunda_orchestration_sdk.runtime.clock import ManualClock
from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
)
from camunda_orchestration_sdk.semantic_types import JobKey


_CONFIG: CamundaSdkConfigPartial = {"CAMUNDA_REST_ADDRESS": "http://api.local/v2"}

#: A body the SDK can parse into a TopologyResponse, so a 200 is a genuine success.
_TOPOLOGY_OK: dict[str, Any] = {
    "brokers": [],
    "clusterId": None,
    "clusterSize": 1,
    "partitionsCount": 1,
    "replicationFactor": 1,
    "gatewayVersion": "8.8.0",
    "lastCompletedChangeId": "0",
}


def _problem(title: str, status: int) -> dict[str, Any]:
    """A complete RFC 7807 body, so the SDK raises its typed error rather than
    failing to parse -- which would never reach the backpressure branch at all."""

    return {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": title,
        "instance": "/topology",
    }

#: (status, body, is a backpressure signal). A bare 503 counts; a 503 that explains
#: itself as something else does not, and neither does a plain 500.
_RESPONSE_CASES: list[tuple[str, int, dict[str, Any] | None, bool]] = [
    ("429", 429, {"title": "TOO_MANY_REQUESTS"}, True),
    ("bare-503", 503, None, True),
    ("500-resource-exhausted", 500, _problem("RESOURCE_EXHAUSTED", 500), True),
    ("500-plain", 500, _problem("INTERNAL_ERROR", 500), False),
    ("503-other", 503, {"title": "SOMETHING_ELSE"}, False),
]


class _RecordingBackpressure:
    """Delegates to the real manager and counts what the client asked of it."""

    def __init__(self, inner: Any) -> None:
        self.inner = inner
        self.acquires = 0
        self.releases = 0
        self.backpressure_signals = 0
        self.healthy_hints = 0

    def acquire(self) -> None:
        self.acquires += 1
        self.inner.acquire()

    def release(self) -> None:
        self.releases += 1
        self.inner.release()

    def record_backpressure(self) -> None:
        self.backpressure_signals += 1
        self.inner.record_backpressure()

    def record_healthy_hint(self) -> None:
        self.healthy_hints += 1
        self.inner.record_healthy_hint()

    def get_state(self) -> Any:
        return self.inner.get_state()


def _response(status: int, body: dict[str, Any] | None) -> Callable[
    [httpx.Request], httpx.Response
]:
    def handler(request: httpx.Request) -> httpx.Response:
        if body is None:
            return httpx.Response(status, request=request)
        return httpx.Response(status, json=body, request=request)

    return handler


def _sync_client(
    handler: Callable[[httpx.Request], httpx.Response], clock: ManualClock
) -> CamundaClient:
    return CamundaClient(
        configuration=_CONFIG,
        clock=clock,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )


def _async_client(
    handler: Callable[[httpx.Request], httpx.Response], clock: ManualClock
) -> CamundaAsyncClient:
    return CamundaAsyncClient(
        configuration=_CONFIG,
        clock=clock,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )


# --- which responses gate -----------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "status", "body", "is_backpressure"),
    _RESPONSE_CASES,
    ids=[case[0] for case in _RESPONSE_CASES],
)
def test_a_response_gates_the_client_only_when_it_signals_backpressure_sync(
    name: str, status: int, body: dict[str, Any] | None, is_backpressure: bool
) -> None:
    client = _sync_client(_response(status, body), ManualClock(start=1000.0))

    assert client._bp.get_state()["permits_max"] is None, "starts unlimited"

    with pytest.raises(errors.ApiError):
        client.get_topology()

    state = client._bp.get_state()
    if is_backpressure:
        assert state["permits_max"] is not None, (
            f"{name} should have left the unlimited state"
        )
        assert state["severity"] == "soft"
        assert state["consecutive"] == 1
    else:
        assert state["permits_max"] is None, f"{name} is not a backpressure signal"
        assert state["severity"] == "healthy"
        assert state["consecutive"] == 0


@pytest.mark.parametrize(
    ("name", "status", "body", "is_backpressure"),
    _RESPONSE_CASES,
    ids=[case[0] for case in _RESPONSE_CASES],
)
@pytest.mark.asyncio
async def test_a_response_gates_the_client_only_when_it_signals_backpressure_async(
    name: str, status: int, body: dict[str, Any] | None, is_backpressure: bool
) -> None:
    client = _async_client(_response(status, body), ManualClock(start=1000.0))

    assert client._bp.get_state()["permits_max"] is None

    with pytest.raises(errors.ApiError):
        await client.get_topology()

    state = client._bp.get_state()
    if is_backpressure:
        assert state["permits_max"] is not None, (
            f"{name} should have left the unlimited state"
        )
        assert state["severity"] == "soft"
    else:
        assert state["permits_max"] is None, f"{name} is not a backpressure signal"
        assert state["severity"] == "healthy"


def test_repeated_backpressure_escalates_to_severe_and_lowers_the_cap_sync() -> None:
    client = _sync_client(_response(429, {"title": "T"}), ManualClock(start=1000.0))

    caps: list[Any] = []
    for _ in range(3):
        with pytest.raises(errors.ApiError):
            client.get_topology()
        caps.append(client._bp.get_state()["permits_max"])

    assert caps[0] is not None
    assert caps == sorted(caps, reverse=True), f"cap must not grow under load: {caps}"
    assert caps[-1] < caps[0]
    assert client._bp.get_state()["severity"] == "severe"


# --- the gate is actually consulted, and bypassed where it must be ------------------


def test_a_gated_method_takes_and_returns_a_permit_sync() -> None:
    client = _sync_client(
        lambda request: httpx.Response(200, json=_TOPOLOGY_OK, request=request),
        ManualClock(start=1000.0),
    )
    spy = _RecordingBackpressure(client._bp)
    client._bp = cast(BackpressureManager, spy)

    client.get_topology()

    assert (spy.acquires, spy.releases, spy.healthy_hints) == (1, 1, 1)
    assert spy.backpressure_signals == 0


def test_a_bypass_listed_method_is_not_gated_sync() -> None:
    """Completion work must drain even when the gate is closed."""

    client = _sync_client(
        lambda request: httpx.Response(204, request=request),
        ManualClock(start=1000.0),
    )
    spy = _RecordingBackpressure(client._bp)
    client._bp = cast(BackpressureManager, spy)

    client.complete_job(job_key=JobKey("2251799813653498"))

    assert spy.acquires == 0
    assert spy.releases == 0


def test_a_bypass_listed_method_still_runs_with_every_permit_taken_sync() -> None:
    """The real test of a bypass: not a lowered cap, but no permits left at all."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and "completion" in str(request.url):
            return httpx.Response(204, request=request)
        return httpx.Response(429, json={"title": "T"}, request=request)

    client = _sync_client(handler, ManualClock(start=1000.0))

    with pytest.raises(errors.ApiError):
        client.get_topology()

    permits_max = client._bp.get_state()["permits_max"]
    assert permits_max is not None, "the gate should have a finite cap by now"
    for _ in range(permits_max):
        client._bp.acquire()
    state = client._bp.get_state()
    assert state["permits_current"] == state["permits_max"], "gate is saturated"

    # Run the completion on another thread: if a routing regression ever gated it, it
    # would block on the semaphore forever, and this fails in seconds instead of
    # hanging CI. The timeout is a safety net, not a correctness signal -- the
    # assertion is that completion does not wait for a permit at all.
    finished = threading.Event()
    raised: list[BaseException] = []

    def _complete() -> None:
        try:
            client.complete_job(job_key=JobKey("2251799813653498"))
        except BaseException as exc:
            raised.append(exc)
        finally:
            finished.set()

    threading.Thread(target=_complete, daemon=True).start()

    assert finished.wait(timeout=10.0), (
        "completion blocked on the backpressure gate; drain work must bypass it"
    )
    assert raised == []


# --- the hook regression this is really about ---------------------------------------


def _generated_api_methods(cls: type) -> dict[str, str]:
    """Source of every generated API wrapper on ``cls``, by method name."""

    methods: dict[str, str] = {}
    for name, member in vars(cls).items():
        if name.startswith("_") or not inspect.isfunction(member):
            continue
        source = inspect.getsource(member)
        if '_kwargs["client"] = self.client' not in source:
            continue
        methods[name] = source
    return methods


@pytest.mark.parametrize(
    ("client_cls", "gate_call"),
    [
        (CamundaClient, "self._bp.acquire()"),
        # Spelled with the await: on the async client a bare ``self._bp.acquire()``
        # creates a coroutine and discards it, taking no permit at all, and the
        # substring without ``await`` would accept that as gating.
        (CamundaAsyncClient, "await self._bp.acquire()"),
    ],
    ids=["sync", "async"],
)
def test_every_generated_method_is_gated_except_the_bypass_set(
    client_cls: type, gate_call: str
) -> None:
    methods = _generated_api_methods(client_cls)
    assert len(methods) > 50, "expected the generated API surface, got almost nothing"

    ungated = {name for name, source in methods.items() if gate_call not in source}

    assert ungated == set(EXEMPT_METHODS) & set(methods), (
        "exactly the bypass-listed methods may skip the backpressure gate"
    )


def test_every_bypass_listed_method_exists_on_the_client() -> None:
    """The bypass set must not drift away from the generated surface."""

    assert set(EXEMPT_METHODS) <= set(_generated_api_methods(CamundaClient))


# --- recovery -----------------------------------------------------------------------


def test_the_gate_reopens_after_sustained_healthy_traffic_sync() -> None:
    state: dict[str, bool] = {"fail": True}

    def handler(request: httpx.Request) -> httpx.Response:
        if state["fail"]:
            return httpx.Response(429, json={"title": "T"}, request=request)
        return httpx.Response(200, json=_TOPOLOGY_OK, request=request)

    clock = ManualClock(start=1000.0)
    client = _sync_client(handler, clock)

    with pytest.raises(errors.ApiError):
        client.get_topology()
    assert client._bp.get_state()["permits_max"] is not None

    state["fail"] = False

    # Quiet long enough for severity to decay back to healthy...
    clock.advance_sync(5.0)
    client.get_topology()
    assert client._bp.get_state()["severity"] == "healthy"

    # ...then sustained healthy for the unlimited threshold.
    clock.advance_sync(31.0)
    client.get_topology()
    assert client._bp.get_state()["permits_max"] is None, (
        "permits should return to unlimited after sustained healthy traffic"
    )
