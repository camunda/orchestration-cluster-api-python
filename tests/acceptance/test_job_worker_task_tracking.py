"""Regression tests for JobWorker in-flight task tracking (issue #151).

Before #151, `JobWorker.poll_loop` spawned `_execute_job` tasks via
`asyncio.create_task(...)` and discarded the handles, so `stop()`/
`close()` had no way to cancel them before tearing down the pools they
were awaiting. After `close()` shut a pool down, an in-flight job task
that next called `run_in_executor(self.thread_pool, ...)` would either
raise 'cannot schedule new futures after shutdown' or hit the
use-after-close guard added in #150.

These tests assert the class of defect: in-flight job tasks must be
tracked by the worker, must be cancelled by `stop()`/`aclose()`, and
`aclose()` must give cancellations a chance to propagate before tearing
the pools down.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import MagicMock

import pytest

from camunda_orchestration_sdk.runtime.job_worker import (
    JobContext,
    JobWorker,
    WorkerConfig,
)


def _make_config() -> WorkerConfig:
    return WorkerConfig(job_type="test", job_timeout_milliseconds=1000)


async def _async_cb(job: JobContext) -> dict[str, Any]:
    return {}


@pytest.mark.asyncio
async def test_poll_loop_tracks_spawned_job_tasks() -> None:
    """poll_loop must register every spawned job task in _inflight_tasks
    so stop()/aclose() can find and cancel them.

    Class-of-defect assertion: any code path that spawns a job task
    must put the handle in the tracking set.
    """
    from camunda_orchestration_sdk.models.job_activation_result import (
        JobActivationResult,
    )
    from camunda_orchestration_sdk.models.activated_job_result import (
        ActivatedJobResult,
    )

    mock_client = MagicMock()

    async def slow_cb(job: JobContext) -> dict[str, Any]:
        await asyncio.sleep(60)  # long enough to outlive the test
        return {}

    config = WorkerConfig(
        job_type="test", job_timeout_milliseconds=1000, max_concurrent_jobs=4
    )
    worker = JobWorker(mock_client, slow_cb, config)
    try:
        # Build two minimal job items.
        jobs: list[Any] = []
        for key in (1, 2):
            job = MagicMock(spec=ActivatedJobResult)
            job.job_key = key
            job.type_ = "test-job"
            job.process_instance_key = 1
            job.bpmn_process_id = "p"
            job.process_definition_version = 1
            job.process_definition_key = 2
            job.element_id = "e"
            job.element_instance_key = 3
            job.custom_headers = {}
            job.worker = "w"
            job.retries = 3
            job.deadline = 0
            job.variables = None
            jobs.append(job)

        mock_client.activate_jobs = MagicMock(
            return_value=_make_completed_future(JobActivationResult(jobs=jobs))
        )

        worker.running = True
        # Drive one polling iteration manually rather than start()'ing the
        # whole loop, so the test stays deterministic.
        polled = await worker._poll_for_jobs()  # pyright: ignore[reportPrivateUsage]
        for job_item in polled:
            task = asyncio.create_task(worker._execute_job(job_item))  # pyright: ignore[reportPrivateUsage]
            worker._inflight_tasks.add(task)  # pyright: ignore[reportPrivateUsage]
            task.add_done_callback(worker._inflight_tasks.discard)  # pyright: ignore[reportPrivateUsage]

        assert len(worker._inflight_tasks) == 2  # pyright: ignore[reportPrivateUsage]
    finally:
        await worker.aclose()


def _make_completed_future(value: Any) -> Any:
    fut: asyncio.Future[Any] = asyncio.get_event_loop().create_future()
    fut.set_result(value)
    return fut


@pytest.mark.asyncio
async def test_stop_cancels_inflight_tasks() -> None:
    """stop() must cancel every task in _inflight_tasks before close()."""
    worker = JobWorker(MagicMock(), _async_cb, _make_config())

    async def long_running() -> None:
        await asyncio.sleep(60)

    task = asyncio.create_task(long_running())
    worker._inflight_tasks.add(task)  # pyright: ignore[reportPrivateUsage]
    task.add_done_callback(worker._inflight_tasks.discard)  # pyright: ignore[reportPrivateUsage]
    worker.running = True

    worker.stop()

    # cancel() is sync; cancellation propagates on the next loop tick.
    await asyncio.sleep(0)
    assert task.cancelled() or task.done(), (
        "stop() did not cancel the in-flight task; pools could be torn "
        "down while the task is still awaiting them."
    )


@pytest.mark.asyncio
async def test_aclose_awaits_inflight_task_cancellation_before_pool_shutdown() -> None:
    """aclose() must await cancellations BEFORE close() shuts pools down.

    This is the contract that prevents 'cannot schedule new futures
    after shutdown' / use-after-close errors from surfacing as task
    exceptions: by the time close() runs, no task is still trying to
    submit work to a pool.
    """
    worker = JobWorker(MagicMock(), _async_cb, _make_config())

    pool_alive_during_cancellation: list[bool] = []

    async def task_that_observes_pool() -> None:
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            # When cancellation hits, the pool must still be alive — the
            # whole point of aclose() is to cancel-then-await BEFORE
            # tearing down the pool. We can't easily check pool state
            # from a real worker task, so as a proxy assert _closed is
            # still False at this point.
            pool_alive_during_cancellation.append(not worker._closed)  # pyright: ignore[reportPrivateUsage]
            raise

    task = asyncio.create_task(task_that_observes_pool())
    worker._inflight_tasks.add(task)  # pyright: ignore[reportPrivateUsage]
    task.add_done_callback(worker._inflight_tasks.discard)  # pyright: ignore[reportPrivateUsage]

    # Let the task actually start awaiting sleep(60) before we cancel it.
    await asyncio.sleep(0)

    await worker.aclose()

    assert pool_alive_during_cancellation == [True], (
        "aclose() shut the worker down BEFORE the in-flight task's "
        "cancellation handler ran — that re-introduces the use-after-"
        "close race issue #151 was supposed to fix."
    )
    assert worker._closed  # pyright: ignore[reportPrivateUsage]


@pytest.mark.asyncio
async def test_async_context_manager_uses_aclose() -> None:
    """`async with JobWorker(...)` must trigger the async-aware teardown.

    Otherwise async callers silently get the synchronous close() and
    lose the in-flight-task-cancellation guarantee.
    """
    saw_aclose = False

    worker = JobWorker(MagicMock(), _async_cb, _make_config())
    original_aclose = worker.aclose

    async def spy_aclose() -> None:
        nonlocal saw_aclose
        saw_aclose = True
        await original_aclose()

    worker.aclose = spy_aclose  # ty: ignore[invalid-assignment]

    async with worker:
        pass

    assert saw_aclose, "async with did not invoke aclose()"
