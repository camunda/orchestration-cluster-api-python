"""Job-lease behaviour: the worker opts into leasing, threads the returned token onto the
fenced commands, and refuses an activation whose lease was not honoured.

These exercise the worker end-to-end against a mock client (activation and each of the three
acknowledgement paths), rather than only the pure guard in test_present_when_runtime.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest
from camunda_orchestration_sdk.models.job_error_request import JobErrorRequest
from camunda_orchestration_sdk.models.job_fail_request import JobFailRequest
from camunda_orchestration_sdk.runtime.job_worker import (
    JobError,
    JobFailure,
    JobWorker,
    WorkerConfig,
)
from camunda_orchestration_sdk.runtime.present_when import LeaseNotHonoredError
from camunda_orchestration_sdk.semantic_types import JobLeaseToken


def _job(token: str | None) -> MagicMock:
    job = MagicMock(spec=ActivatedJobResult)
    job.job_key = 12345
    job.retries = 3
    job.job_lease_token = JobLeaseToken(token) if token is not None else None
    return job


def _client(jobs: list[Any] | None = None) -> MagicMock:
    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=jobs or []))
    return client


@pytest.mark.parametrize("with_lease,expected", [(False, None), (True, True)])
def test_activation_opts_into_lease_only_when_asked(with_lease: bool, expected: Any) -> None:
    import asyncio

    client = _client()
    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=with_lease)
    worker = JobWorker(client, lambda job: {}, config)

    asyncio.run(worker._poll_for_jobs())  # pyright: ignore[reportPrivateUsage]

    data = client.activate_jobs.call_args.kwargs["data"]
    # False leaves the field unset (UNSET, not sent); True sends withLease=true.
    if expected is None:
        assert data.with_lease is not True
    else:
        assert data.with_lease is True


def test_poll_rejects_an_unhonored_lease() -> None:
    import asyncio

    # Leased activation, but the server returned a job with no token.
    client = _client(jobs=[_job(None)])
    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, lambda job: {}, config)

    with pytest.raises(LeaseNotHonoredError):
        asyncio.run(worker._poll_for_jobs())  # pyright: ignore[reportPrivateUsage]


def test_poll_accepts_a_honored_lease() -> None:
    import asyncio

    client = _client(jobs=[_job("lease-abc")])
    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, lambda job: {}, config)

    jobs = asyncio.run(worker._poll_for_jobs())  # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 1


@pytest.mark.asyncio
async def test_lease_token_threaded_into_completion() -> None:
    client = _client()

    async def callback(job: Any) -> dict[str, Any]:
        return {"ok": True}

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    data = client.complete_job.call_args.kwargs["data"]
    assert isinstance(data, JobCompletionRequest)
    assert data.job_lease_token == "lease-abc"


@pytest.mark.asyncio
async def test_lease_token_threaded_into_failure() -> None:
    client = _client()

    async def callback(job: Any) -> dict[str, Any]:
        raise JobFailure("boom", retries=1)

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    data = client.fail_job.call_args.kwargs["data"]
    assert isinstance(data, JobFailRequest)
    assert data.job_lease_token == "lease-abc"


@pytest.mark.asyncio
async def test_lease_token_threaded_into_error() -> None:
    client = _client()

    async def callback(job: Any) -> dict[str, Any]:
        raise JobError("E1", "nope")

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    data = client.throw_job_error.call_args.kwargs["data"]
    assert isinstance(data, JobErrorRequest)
    assert data.job_lease_token == "lease-abc"


@pytest.mark.asyncio
async def test_unleased_job_carries_no_token() -> None:
    client = _client()

    async def callback(job: Any) -> dict[str, Any]:
        return {"ok": True}

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job(None))  # pyright: ignore[reportPrivateUsage]

    data = client.complete_job.call_args.kwargs["data"]
    # When the job was not leased the token field stays at its default (UNSET); the worker
    # never brands a JobLeaseToken onto it.
    assert not isinstance(data.job_lease_token, JobLeaseToken)


@pytest.mark.asyncio
async def test_unhonored_lease_stops_the_worker_rather_than_looping() -> None:
    """A lease-unaware server is a deterministic incompatibility, not a transient poll
    error. The poll loop swallows every exception and retries, so without an explicit
    escape the worker would abandon each activated batch to its timeout forever and the
    caller would never see the failure."""
    client = _client(jobs=[_job(None)])
    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, lambda job: {}, config)
    worker.running = True  # poll_loop is a no-op otherwise

    with pytest.raises(LeaseNotHonoredError):
        await worker.poll_loop()


@pytest.mark.asyncio
async def test_connected_handler_commands_carry_the_lease_token() -> None:
    """A handler that finishes its own job through `job.client` must still present the
    token, or the engine rejects the fenced command."""
    client = _client()

    async def callback(job: Any) -> None:
        await job.client.complete_job(job_key=job.job_key, data=JobCompletionRequest())

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    data = client.complete_job.call_args.kwargs["data"]
    assert data.job_lease_token == "lease-abc"


@pytest.mark.asyncio
async def test_this_jobs_token_overrides_a_stale_one_on_the_body() -> None:
    """The lease token identifies *this* activation, so the worker's per-job token always
    wins over one already on the body — a token from a prior job (see the reuse test) or a
    mismatched one would be rejected by the engine."""
    client = _client()

    async def callback(job: Any) -> None:
        await job.client.complete_job(
            job_key=job.job_key,
            data=JobCompletionRequest(job_lease_token=JobLeaseToken("stale-or-wrong")),
        )

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    assert client.complete_job.call_args.kwargs["data"].job_lease_token == "lease-abc"


def test_reused_request_object_does_not_leak_tokens_between_jobs() -> None:
    """A handler reusing one request object across jobs must not carry the first job's
    token onto the next. The body is copied before injection, so each command gets its own
    job's token and the caller's object is left unmutated."""
    from camunda_orchestration_sdk.runtime.job_worker import _with_lease_token

    shared = JobCompletionRequest()
    k1 = _with_lease_token({"data": shared}, "job-1-token")
    k2 = _with_lease_token({"data": shared}, "job-2-token")

    assert k1["data"].job_lease_token == "job-1-token"
    assert k2["data"].job_lease_token == "job-2-token"
    # The caller's object is never mutated, and the two commands are distinct copies.
    assert k1["data"] is not shared
    assert k2["data"] is not k1["data"]
    assert not isinstance(shared.job_lease_token, JobLeaseToken)



@pytest.mark.asyncio
async def test_system_error_fallback_fail_carries_the_lease_token() -> None:
    """The best-effort fail in the outer handler is still a fenced command: unfenced, it
    could mutate a superseded activation."""
    client = _client()
    # Make the normal completion path blow up so the outer handler's fallback runs.
    client.complete_job = AsyncMock(side_effect=RuntimeError("transport exploded"))

    async def callback(job: Any) -> dict[str, Any]:
        return {"ok": True}

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    client.fail_job.assert_called_once()
    assert client.fail_job.call_args.kwargs["data"].job_lease_token == "lease-abc"


@pytest.mark.asyncio
async def test_connected_handler_omitted_body_still_carries_the_token() -> None:
    """`complete_job` and `fail_job` accept an omitted body (`data=UNSET`). A leased job
    still has to present its token, so the empty body is synthesized rather than the
    fencing being silently dropped."""
    for op, factory_type in (("complete_job", JobCompletionRequest), ("fail_job", JobFailRequest)):
        client = _client()

        async def callback(job: Any, _op: str = op) -> None:
            await getattr(job.client, _op)(job_key=job.job_key)

        config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
        worker = JobWorker(client, callback, config)

        await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

        data = getattr(client, op).call_args.kwargs["data"]
        assert isinstance(data, factory_type), f"{op}: expected a synthesized {factory_type.__name__}"
        assert data.job_lease_token == "lease-abc", f"{op}: lease token dropped"


@pytest.mark.asyncio
async def test_unleased_omitted_body_is_left_alone() -> None:
    """Without a lease there is nothing to fence, so an omitted body stays omitted."""
    client = _client()

    async def callback(job: Any) -> None:
        await job.client.complete_job(job_key=job.job_key)

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job(None))  # pyright: ignore[reportPrivateUsage]

    assert "data" not in client.complete_job.call_args.kwargs


@pytest.mark.asyncio
async def test_stopping_on_an_unhonored_lease_clears_the_running_flag() -> None:
    """The polling task has terminated, so the worker must not still look live: otherwise
    lifecycle code reports a running worker and a later start() is a no-op."""
    client = _client(jobs=[_job(None)])
    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, lambda job: {}, config)
    worker.running = True

    with pytest.raises(LeaseNotHonoredError):
        await worker.poll_loop()

    assert worker.running is False


# --- Both job-scoped wrappers, all three terminal operations -------------------------
#
# A sync handler defaults to the "thread" strategy, so `_JobScopedSyncClient` is the
# *default* path for synchronous handlers. Parametrized over both wrappers so a fence
# missing from either one fails here, rather than only the async path being covered.

_TERMINAL_OPS = [
    ("complete_job", JobCompletionRequest, {}),
    ("fail_job", JobFailRequest, {"retries": 1}),
    ("throw_job_error", JobErrorRequest, {"error_code": "E1"}),
]


def _wrapper(kind: str, inner: Any, lease_token: str | None) -> Any:
    from camunda_orchestration_sdk.runtime.job_worker import (
        _AckFlag,
        _JobScopedAsyncClient,
        _JobScopedSyncClient,
    )

    cls = _JobScopedAsyncClient if kind == "async" else _JobScopedSyncClient
    return cls(inner, "12345", _AckFlag(), lease_token)


@pytest.mark.parametrize("kind", ["async", "sync"])
@pytest.mark.parametrize("op,body_cls,body_kwargs", _TERMINAL_OPS)
@pytest.mark.asyncio
async def test_both_wrappers_fence_every_terminal_operation(
    kind: str, op: str, body_cls: Any, body_kwargs: dict[str, Any]
) -> None:
    inner = MagicMock()
    setattr(inner, op, AsyncMock() if kind == "async" else MagicMock())
    wrapped = _wrapper(kind, inner, "lease-abc")

    call = getattr(wrapped, op)("12345", data=body_cls(**body_kwargs))
    if kind == "async":
        await call

    sent = getattr(inner, op).call_args.kwargs["data"]
    assert sent.job_lease_token == "lease-abc", f"{kind} wrapper dropped the token on {op}"


@pytest.mark.parametrize("kind", ["async", "sync"])
@pytest.mark.asyncio
async def test_both_wrappers_leave_another_jobs_command_alone(kind: str) -> None:
    """The fence is scoped to *this* job; a command for a different job must not be
    stamped with this job's token."""
    inner = MagicMock()
    inner.complete_job = AsyncMock() if kind == "async" else MagicMock()
    wrapped = _wrapper(kind, inner, "lease-abc")

    call = wrapped.complete_job(99999, data=JobCompletionRequest())
    if kind == "async":
        await call

    sent = inner.complete_job.call_args.kwargs["data"]
    assert not isinstance(sent.job_lease_token, JobLeaseToken)


@pytest.mark.asyncio
async def test_thread_strategy_wires_the_lease_token_into_the_sync_wrapper() -> None:
    """End-to-end for the sync path: a synchronous connected handler finishing its own
    job through `job.client` must still present the token."""
    client = _client()
    sync_inner = MagicMock()
    sync_inner.complete_job = MagicMock()

    def callback(job: Any) -> None:
        job.client.complete_job(job_key=job.job_key, data=JobCompletionRequest())

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)
    assert worker._strategy == "thread", "a sync handler must default to the thread strategy"  # pyright: ignore[reportPrivateUsage]
    worker._sync_client = sync_inner  # pyright: ignore[reportPrivateUsage]

    await worker._execute_job(_job("lease-abc"))  # pyright: ignore[reportPrivateUsage]

    sync_inner.complete_job.assert_called_once()
    assert sync_inner.complete_job.call_args.kwargs["data"].job_lease_token == "lease-abc"


def _wire_activation_job() -> dict[str, Any]:
    """A job as a server sends it on the activate-jobs response, with no lease token."""
    return {
        "type": "t",
        "processDefinitionId": "p",
        "processDefinitionVersion": 1,
        "elementId": "e",
        "customHeaders": {},
        "worker": "w",
        "retries": 3,
        "deadline": 1_700_000_000_000,
        "variables": {},
        "tenantId": "<default>",
        "jobKey": "1",
        "processInstanceKey": "2",
        "processDefinitionKey": "3",
        "elementInstanceKey": "4",
        "kind": "BPMN_ELEMENT",
        "listenerEventType": "UNSPECIFIED",
        "userTask": None,
        "tags": [],
        "rootProcessInstanceKey": None,
        "businessId": None,
        "priority": 0,
        "physicalTenantId": "pt",
    }


@pytest.mark.asyncio
async def test_run_workers_surfaces_an_unhonored_lease() -> None:
    """The terminal failure must reach the caller through the public path. `run_workers`
    blocks on an unset event and previously never observed the polling tasks, so the raise
    from `poll_loop` was reduced to an unobserved-task warning while the caller ran on."""
    import asyncio

    import httpx

    from camunda_orchestration_sdk import CamundaAsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/jobs/activation"):
            return httpx.Response(200, json={"jobs": [_wire_activation_job()]})
        return httpx.Response(204)

    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(handler)})
    client.create_job_worker(
        WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True),
        lambda job: {},
    )

    with pytest.raises(LeaseNotHonoredError):
        await asyncio.wait_for(client.run_workers(), timeout=5)


@pytest.mark.asyncio
async def test_returned_completion_object_is_not_mutated_across_jobs() -> None:
    """The automatic-action path: when a handler returns a shared `JobCompletionRequest`,
    the worker must not write each job's token into that one object — with concurrent jobs
    reusing it, one command could serialize with another activation's token."""
    client = _client()
    shared = JobCompletionRequest()

    async def callback(job: Any) -> JobCompletionRequest:
        return shared

    config = WorkerConfig(job_type="t", job_timeout_milliseconds=1000, with_lease=True)
    worker = JobWorker(client, callback, config)

    await worker._execute_job(_job("token-1"))  # pyright: ignore[reportPrivateUsage]
    await worker._execute_job(_job("token-2"))  # pyright: ignore[reportPrivateUsage]

    calls = client.complete_job.call_args_list
    assert calls[0].kwargs["data"].job_lease_token == "token-1"
    assert calls[1].kwargs["data"].job_lease_token == "token-2"
    # The caller's object is never mutated.
    assert not isinstance(shared.job_lease_token, JobLeaseToken)


@pytest.mark.asyncio
async def test_run_workers_retrieves_every_concurrent_failure() -> None:
    """When several polling tasks fail in the same batch, `run_workers` must retrieve every
    one's exception, or the un-inspected ones warn as `Task exception was never retrieved`
    at teardown and mask concurrent failures. Only the first is propagated."""
    import asyncio
    from typing import cast

    from camunda_orchestration_sdk import CamundaAsyncClient

    async def boom() -> None:
        raise LeaseNotHonoredError("k", "withLease")

    t1 = asyncio.ensure_future(boom())
    t2 = asyncio.ensure_future(boom())
    # Wait for both to fail without retrieving their exceptions (asyncio.wait does not),
    # so run_workers is the first to observe them.
    await asyncio.wait({t1, t2})

    class _FakeWorker:
        def __init__(self, task: "asyncio.Task[None]") -> None:
            self.polling_task = task

        async def aclose(self) -> None:
            pass

    client = CamundaAsyncClient()
    client._workers = cast(Any, [_FakeWorker(t1), _FakeWorker(t2)])

    with pytest.raises(LeaseNotHonoredError):
        await client.run_workers()

    # `_log_traceback` is the flag asyncio checks at GC to emit the never-retrieved warning;
    # False on both means run_workers inspected every failure, not just the first.
    assert cast(Any, t1)._log_traceback is False
    assert cast(Any, t2)._log_traceback is False, "a concurrent worker failure was left unretrieved"
