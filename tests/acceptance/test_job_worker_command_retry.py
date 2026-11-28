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
