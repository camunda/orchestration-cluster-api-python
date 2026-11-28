"""Job command retry policy (issue #498).

Job commands are not idempotent, so the worker retries them only when the server says the
command was NOT applied (429 / 503 / connect failure before send). Any status or transport
error that leaves the outcome unknown (500 / 502 / 504, read timeout, reset after send) is
sent exactly once, and the worker sends no follow-up ``fail_job``. A 404 is logged as
"job not found" without a follow-up ``fail_job`` either.

These run the worker against a real ``CamundaAsyncClient`` on an ``httpx.MockTransport`` so
the whole path (generated error mapping included) is covered for every job command.
"""

from __future__ import annotations

from typing import Any, Callable
from unittest.mock import MagicMock

import httpx
import pytest

from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.runtime.job_worker import (
    JobError,
    JobFailure,
    JobWorker,
    WorkerConfig,
    classify_job_command_error,
)

def _complete(job: Any) -> dict[str, Any]:
    return {"ok": True}


def _fail(job: Any) -> Any:
    raise JobFailure("nope", retries=1)


def _error(job: Any) -> Any:
    raise JobError("E1", "bpmn error")


# command -> (handler that triggers it, URL suffix it posts to)
_COMMANDS: dict[str, tuple[Callable[[Any], Any], str]] = {
    "complete": (_complete, "/completion"),
    "fail": (_fail, "/failure"),
    "error": (_error, "/error"),
}


def _job() -> MagicMock:
    job = MagicMock(spec=ActivatedJobResult)
    job.job_key = "12345"
    job.retries = 3
    job.job_lease_token = None
    return job


class _Recorder:
    def __init__(self, command_suffix: str, responder: Callable[[int], httpx.Response]):
        self.suffix = command_suffix
        self.responder = responder
        self.command_requests = 0
        self.paths: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.paths.append(request.url.path)
        if request.url.path.endswith(self.suffix):
            self.command_requests += 1
            return self.responder(self.command_requests)
        return httpx.Response(204)


def _worker(recorder: _Recorder, callback: Callable[[Any], Any]) -> JobWorker:
    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(recorder)})
    worker = JobWorker(
        client, callback, WorkerConfig(job_type="t", job_timeout_milliseconds=1000)
    )
    worker._job_command_backoff_base_s = 0.001  # pyright: ignore[reportPrivateUsage]
    worker._job_command_backoff_max_s = 0.001  # pyright: ignore[reportPrivateUsage]
    return worker


def _status(code: int) -> Callable[[int], httpx.Response]:
    return lambda _n: httpx.Response(
        code, json={"type": "about:blank", "title": "x", "status": code, "detail": "x", "instance": "/"}
    )


def _raise(exc: Exception) -> Callable[[int], httpx.Response]:
    def responder(_n: int) -> httpx.Response:
        raise exc

    return responder


_UNKNOWN_OUTCOMES: dict[str, Callable[[int], httpx.Response]] = {
    "504": _status(504),
    "502": _status(502),
    "500": _status(500),
    "read-timeout": _raise(httpx.ReadTimeout("read timed out")),
    "reset-after-send": _raise(httpx.RemoteProtocolError("connection reset")),
    "read-error": _raise(httpx.ReadError("connection reset by peer")),
}


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
@pytest.mark.parametrize("outcome", sorted(_UNKNOWN_OUTCOMES))
async def test_unknown_outcome_is_sent_once_with_no_follow_up_fail(
    command: str, outcome: str
) -> None:
    callback, suffix = _COMMANDS[command]
    recorder = _Recorder(suffix, _UNKNOWN_OUTCOMES[outcome])
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 1
    # No follow-up fail_job (other than the command itself when it IS fail_job).
    fail_calls = [p for p in recorder.paths if p.endswith("/failure")]
    assert len(fail_calls) == (1 if command == "fail" else 0)


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
@pytest.mark.parametrize("code", [429, 503, "500-resource-exhausted"])
async def test_not_applied_status_is_retried(command: str, code: int | str) -> None:
    callback, suffix = _COMMANDS[command]

    def rejected(_n: int) -> httpx.Response:
        if code == "500-resource-exhausted":
            return httpx.Response(
                500,
                json={"type": "about:blank", "title": "RESOURCE_EXHAUSTED", "status": 500,
                      "detail": "RESOURCE_EXHAUSTED", "instance": "/"},
            )
        assert isinstance(code, int)
        return _status(code)(_n)

    def responder(n: int) -> httpx.Response:
        return rejected(n) if n < 3 else httpx.Response(204)

    recorder = _Recorder(suffix, responder)
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 3
    fail_calls = [p for p in recorder.paths if p.endswith("/failure")]
    assert len(fail_calls) == (3 if command == "fail" else 0)


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
async def test_connect_failure_before_send_is_retried(command: str) -> None:
    callback, suffix = _COMMANDS[command]

    def responder(n: int) -> httpx.Response:
        if n < 2:
            raise httpx.ConnectError("connection refused")
        return httpx.Response(204)

    recorder = _Recorder(suffix, responder)
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
async def test_not_found_is_not_retried_and_sends_no_follow_up_fail(command: str) -> None:
    callback, suffix = _COMMANDS[command]
    recorder = _Recorder(suffix, _status(404))
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 1
    fail_calls = [p for p in recorder.paths if p.endswith("/failure")]
    assert len(fail_calls) == (1 if command == "fail" else 0)


@pytest.mark.parametrize(
    "exc,expected",
    [
        (httpx.ConnectError("x"), "retry"),
        (httpx.ConnectTimeout("x"), "retry"),
        (httpx.ReadTimeout("x"), "unknown"),
        (httpx.WriteTimeout("x"), "unknown"),
        (httpx.RemoteProtocolError("x"), "unknown"),
        (RuntimeError("x"), "other"),
    ],
)
def test_classify_transport_errors(exc: Exception, expected: str) -> None:
    assert classify_job_command_error(exc) == expected


# --- Undecodable error bodies keep their HTTP status (all three commands) ---------------
_BAD_BODIES: dict[str, Callable[[int], httpx.Response]] = {
    "empty": lambda code: httpx.Response(code, content=b""),
    "html": lambda code: httpx.Response(
        code, content=b"<html>bad gateway</html>", headers={"content-type": "text/html"}
    ),
    "incomplete-json": lambda code: httpx.Response(code, json={"unexpected": 1}),
}


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
@pytest.mark.parametrize("body", sorted(_BAD_BODIES))
@pytest.mark.parametrize("code", [404, 500])
async def test_undecodable_error_body_sends_no_follow_up_fail(
    command: str, body: str, code: int
) -> None:
    callback, suffix = _COMMANDS[command]
    recorder = _Recorder(suffix, lambda _n: _BAD_BODIES[body](code))
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 1
    fail_calls = [p for p in recorder.paths if p.endswith("/failure")]
    assert len(fail_calls) == (1 if command == "fail" else 0)


@pytest.mark.asyncio
@pytest.mark.parametrize("command", sorted(_COMMANDS))
@pytest.mark.parametrize("body", sorted(_BAD_BODIES))
async def test_undecodable_503_body_is_retried(command: str, body: str) -> None:
    callback, suffix = _COMMANDS[command]
    recorder = _Recorder(
        suffix, lambda n: _BAD_BODIES[body](503) if n < 3 else httpx.Response(204)
    )
    worker = _worker(recorder, callback)

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert recorder.command_requests == 3


def test_every_generated_error_decode_is_tolerant() -> None:
    """Class guard: no generated endpoint decodes a 4xx/5xx body outside a try block."""
    import re
    from pathlib import Path

    import camunda_orchestration_sdk

    api = Path(camunda_orchestration_sdk.__file__).parent / "api"
    strict = re.compile(
        r"if response\.status_code == [45]\d\d:\n[ ]+response_\d+ = [^\n]*response\.json\(\)"
    )
    offenders = [str(p) for p in api.rglob("*.py") if strict.search(p.read_text())]
    assert offenders == []


# --- Handler-issued commands with unknown / not-found outcome --------------------------
def _handler_issues(command: str, swallow: bool, sync: bool) -> Callable[[Any], Any]:
    def call(job: Any) -> Any:
        if command == "complete":
            return job.client.complete_job(job_key=job.job_key)
        if command == "fail":
            from camunda_orchestration_sdk.models.job_fail_request import JobFailRequest

            return job.client.fail_job(job_key=job.job_key, data=JobFailRequest(retries=0))
        from camunda_orchestration_sdk.models.job_error_request import JobErrorRequest

        return job.client.throw_job_error(
            job_key=job.job_key, data=JobErrorRequest(error_code="E")
        )

    if sync:

        def sync_handler(job: Any) -> Any:
            try:
                call(job)
            except Exception:
                if not swallow:
                    raise
            return {"x": 1}

        return sync_handler

    async def async_handler(job: Any) -> Any:
        try:
            await call(job)
        except Exception:
            if not swallow:
                raise
        return {"x": 1}

    return async_handler


@pytest.mark.asyncio
@pytest.mark.parametrize("strategy", ["async", "thread"])
@pytest.mark.parametrize("command", sorted(_COMMANDS))
@pytest.mark.parametrize("outcome", ["504", "404", "read-timeout"])
@pytest.mark.parametrize("swallow", [True, False])
async def test_handler_command_with_uncertain_outcome_suppresses_auto_action(
    strategy: str, command: str, outcome: str, swallow: bool
) -> None:
    responders: dict[str, Callable[[int], httpx.Response]] = {
        "504": _status(504),
        "404": _status(404),
        "read-timeout": _raise(httpx.ReadTimeout("read timed out")),
    }
    _, suffix = _COMMANDS[command]
    recorder = _Recorder(suffix, responders[outcome])
    sent: list[str] = []

    def transport(request: httpx.Request) -> httpx.Response:
        sent.append(request.url.path)
        return recorder(request)

    handler = _handler_issues(command, swallow, sync=strategy == "thread")
    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(transport)})
    worker = JobWorker(
        client,
        handler,
        WorkerConfig(job_type="t", job_timeout_milliseconds=1000),
        execution_strategy="thread" if strategy == "thread" else "async",
    )
    if strategy == "thread":
        from camunda_orchestration_sdk import CamundaClient

        worker._sync_client = CamundaClient(  # pyright: ignore[reportPrivateUsage]
            httpx_args={"transport": httpx.MockTransport(transport)}
        )

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    # Only the handler's own command went out: no auto-complete, no auto/fallback fail.
    assert len(sent) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("fallback_status", [504, 404])
async def test_fallback_fail_job_uncertain_outcome_is_warned(
    fallback_status: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    def transport(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/completion"):
            return _status(400)(1)  # definite rejection -> system error -> fallback fail_job
        if request.url.path.endswith("/failure"):
            return _status(fallback_status)(1)
        return httpx.Response(204)

    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(transport)})
    worker = JobWorker(
        client, _complete, WorkerConfig(job_type="t", job_timeout_milliseconds=1000)
    )
    warnings: list[str] = []
    monkeypatch.setattr(worker.logger, "warning", lambda msg, *a, **k: warnings.append(msg))

    await worker._execute_job(_job())  # pyright: ignore[reportPrivateUsage]

    assert any("fallback fail_job" in w for w in warnings), warnings
