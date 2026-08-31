"""The incident, inverted.

The failure that started all of this: a worker polling for a process that only completes
after the engine's clock moves. Pin the engine and the worker keeps waiting on the real
clock; drive the worker's clock and the engine never reaches the timer. It burns a real
minute either way.

With `EngineClock` there is one clock. The worker's poll interval and the engine's time are
the same quantity, so a minute of engine time passes in real milliseconds -- and, critically,
the engine really is moved: the pins below are the requests a live engine would have received.

This is the acceptance criterion for camunda/orchestration-cluster-api-js#450 in Python. It
is deliberately written against the SDK's real poll loops rather than a stub, because the
defect it guards was precisely that the seam looked correct while the loops ignored it.
"""

from __future__ import annotations

import time as real_time
from unittest.mock import AsyncMock, MagicMock

import pytest

from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult
from camunda_orchestration_sdk.runtime.clock import EngineClock
from camunda_orchestration_sdk.runtime.eventual import (
    ConsistencyOptions,
    EventualConsistencyTimeoutError,
    eventual_poll_async,
)
from camunda_orchestration_sdk.runtime.job_worker import (
    JobWorker,
    SyncJobContext,
    WorkerConfig,
)

#: Engine time the poller spans. A real minute of polling would be unmistakable in the run.
ENGINE_MINUTE_MS = 60_000

#: Real seconds the whole thing may take. A safety net, not a timing assertion.
REAL_BUDGET_S = 5.0


class RecordingEngine:
    """`PUT /clock` is write-only, so the only way to see engine time move is to record the
    pins the SDK sends."""

    def __init__(self) -> None:
        self.pins: list[int] = []

    async def pin_clock(self, *, data, **kwargs) -> None:
        self.pins.append(data.timestamp)

    async def reset_clock(self, **kwargs) -> None: ...


@pytest.mark.asyncio
async def test_a_minute_of_engine_time_passes_in_real_milliseconds() -> None:
    engine = RecordingEngine()
    clock = EngineClock(engine, start=1_700_000_000.0)
    attempts = 0

    async def never_ready() -> None:
        nonlocal attempts
        attempts += 1
        return None

    started = real_time.monotonic()
    with pytest.raises(EventualConsistencyTimeoutError) as caught:
        await eventual_poll_async(
            "getProcessInstance",
            True,
            never_ready,
            ConsistencyOptions(wait_up_to_ms=ENGINE_MINUTE_MS),
            None,
            clock,
        )
    elapsed = real_time.monotonic() - started

    assert attempts > 1, "the poller never retried, so nothing was being waited on"

    assert caught.value.elapsed_ms >= ENGINE_MINUTE_MS, (
        "the poller gave up before a minute of engine time had passed"
    )
    assert elapsed < REAL_BUDGET_S, (
        f"a minute of engine time took {elapsed:.1f}s of real time -- the poll loop is not "
        "resolving through the engine clock"
    )

    # The half that a virtual clock alone cannot give: the engine was really moved.
    assert engine.pins, "engine time never advanced; only the client's view of it did"
    assert engine.pins == sorted(engine.pins), (
        f"engine time went backwards across the poll loop: {engine.pins}"
    )
    assert engine.pins[-1] - engine.pins[0] >= ENGINE_MINUTE_MS - 1_000, (
        f"the engine advanced {engine.pins[-1] - engine.pins[0]}ms, not the ~{ENGINE_MINUTE_MS}ms "
        "the poller waited"
    )


@pytest.mark.asyncio
async def test_the_client_and_the_engine_agree_on_the_time() -> None:
    """The two clocks staying in step is the whole property; drift is the bug."""
    engine = RecordingEngine()
    clock = EngineClock(engine, start=1_700_000_000.0)

    for _ in range(10):
        await clock.sleep(6.0)

    assert clock.now() == pytest.approx(1_700_000_060.0)
    assert engine.pins[-1] == 1_700_000_060_000, (
        "the engine's last pinned time must match what the client thinks the time is"
    )


@pytest.mark.asyncio
async def test_a_thread_strategy_handler_waits_on_engine_time() -> None:
    """The default path for a sync handler, end to end through the real worker.

    A sync callback resolves to the `thread` strategy, so the handler runs off the loop while
    the worker's own poll loop awaits on the same clock. Both have to reach the engine, and
    the handler reaches it through the blocking API `SyncJobContext` documents.
    """
    engine = RecordingEngine()
    clock = EngineClock(engine, start=1_700_000_000.0)
    await clock.pin()
    pins_before_handler = len(engine.pins)

    seen: dict[str, object] = {}

    def handler(job: SyncJobContext) -> None:
        # Verbatim from the SyncJobContext docstring.
        job.clock.sleep_sync(45.0)
        seen["after"] = job.clock.now()

    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=[]))

    worker = JobWorker(
        client,
        handler,
        WorkerConfig(job_type="test", job_timeout_milliseconds=1_000),
        execution_strategy="thread",
        clock=clock,
    )
    worker._sync_client = MagicMock()  # pyright: ignore[reportPrivateUsage]

    job = MagicMock(spec=ActivatedJobResult)
    job.job_key = 1
    job.type_ = "test"
    # Enough of a job that the worker's failure path is legible if the handler raises.
    job.retries = 3
    job.deadline = 0
    job.variables = None
    job.custom_headers = {}

    started = real_time.monotonic()
    try:
        await worker._execute_job(job)  # pyright: ignore[reportPrivateUsage]
    finally:
        await worker.aclose()
    elapsed = real_time.monotonic() - started

    assert seen.get("after") == 1_700_000_045.0, (
        "the handler's wait did not move the clock; it never reached the engine"
    )
    assert len(engine.pins) > pins_before_handler, (
        "the handler waited without the engine hearing about it"
    )
    assert engine.pins[-1] == 1_700_000_045_000
    assert elapsed < REAL_BUDGET_S, (
        f"a 45s handler wait burned {elapsed:.1f}s of real time"
    )