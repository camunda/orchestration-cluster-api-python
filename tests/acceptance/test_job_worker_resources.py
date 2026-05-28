"""Regression tests for JobWorker resource allocation (issue #148).

JobWorker historically allocated, eagerly in __init__:
  - ThreadPoolExecutor
  - ProcessPoolExecutor (self-pipe + lazy-forked workers)
  - asyncio.new_event_loop() (self-pipe)
  - A daemon worker thread

Most worker instances only ever use one execution strategy, so the other
pools are pure FD waste. On macOS (default ulimit -n 256) the acceptance
suite, which constructs many workers without teardown, would exhaust file
descriptors.

These tests assert the class of defect — no eager allocation for resources
the chosen strategy will never use — rather than just one instance.
"""
from __future__ import annotations

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


def _sync_cb(job: JobContext) -> dict[str, Any]:
    return {}


@pytest.mark.parametrize(
    "callback,expected_strategy",
    [
        (_async_cb, "async"),
        (_sync_cb, "thread"),
    ],
)
def test_job_worker_does_not_eagerly_allocate_unused_pools(
    callback: Any, expected_strategy: str
) -> None:
    """Constructing a JobWorker must not create executors it will never use.

    Specifically, no JobWorker should eagerly allocate a ProcessPoolExecutor;
    the process strategy is rare and process pools are expensive (self-pipe
    FDs + forked interpreters on first submit).
    """
    worker = JobWorker(MagicMock(), callback, _make_config())
    try:
        assert worker._strategy == expected_strategy  # pyright: ignore[reportPrivateUsage]
        # Class-of-defect assertion: no pool allocated for a strategy that
        # will never use it. The non-matching pool attribute must be None.
        assert worker._process_pool is None, (  # pyright: ignore[reportPrivateUsage]
            "ProcessPoolExecutor must be lazy — eager allocation leaks FDs "
            "in tests and wastes resources for async/thread workers."
        )
        if expected_strategy != "thread":
            assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]
    finally:
        worker.close()


def test_job_worker_close_is_idempotent() -> None:
    worker = JobWorker(MagicMock(), _sync_cb, _make_config())
    worker.close()
    worker.close()  # must not raise


def test_job_worker_context_manager_shuts_down_pools() -> None:
    """Using JobWorker as a context manager must release any pools it opened."""
    with JobWorker(MagicMock(), _sync_cb, _make_config()) as worker:
        # Touching the property allocates the pool.
        pool = worker.thread_pool
        assert pool is not None
    # After exit, the pool reference is cleared.
    assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]


def test_job_worker_stop_releases_lazily_allocated_pools() -> None:
    """stop() must tear down any pools the worker allocated while running.

    Higher-level teardown (e.g. run_workers()) calls stop(), not close().
    If stop() didn't release pools, workers that executed jobs would still
    leak FDs.
    """
    worker = JobWorker(MagicMock(), _sync_cb, _make_config())
    # Allocate a pool and put the worker in the running state, mimicking a
    # worker that has executed at least one job.
    _ = worker.thread_pool
    assert worker._thread_pool is not None  # pyright: ignore[reportPrivateUsage]
    worker.running = True

    worker.stop()

    assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]
