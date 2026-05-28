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
        # Class-of-defect assertion: construction must allocate **no** pool,
        # regardless of strategy. A worker that is built but never started
        # (common in tests and exploratory code) should hold zero FDs.
        assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]
        assert worker._process_pool is None, (  # pyright: ignore[reportPrivateUsage]
            "ProcessPoolExecutor must be lazy — eager allocation leaks FDs "
            "in tests and wastes resources for async/thread workers."
        )
        assert worker._worker_loop is None  # pyright: ignore[reportPrivateUsage]
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


def test_job_worker_close_from_within_thread_pool_does_not_deadlock() -> None:
    """close() must not self-join when invoked from a pool worker thread.

    ThreadPoolExecutor.shutdown(wait=True) would otherwise try to join
    the calling thread, raising RuntimeError (or hanging). close() must
    detect this and fall back to wait=False for the offending pool.
    """
    import concurrent.futures

    worker = JobWorker(MagicMock(), _sync_cb, _make_config())
    pool = worker.thread_pool  # allocate

    def call_close_from_inside_pool() -> str:
        # We are now running inside one of `pool`'s worker threads. A
        # naive close() would call pool.shutdown(wait=True), try to join
        # us, and either raise RuntimeError or hang.
        worker.close()
        return "ok"

    future = pool.submit(call_close_from_inside_pool)
    # Generous timeout: if close() actually deadlocks this will fail
    # cleanly with TimeoutError rather than hanging the test suite.
    assert future.result(timeout=5.0) == "ok"
    # The pool reference is cleared even though shutdown couldn't wait.
    assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]
    _ = concurrent.futures  # silence "imported but unused" if lint changes


def test_job_worker_close_immediately_after_loop_access_does_not_leak() -> None:
    """close() must stop the worker loop even when called immediately
    after the first worker_loop access, before run_forever() begins.

    The startup handshake (an Event set inside _run_worker_loop) is what
    makes this deterministic — without it, close() would observe
    is_running()==False, skip the stop callback, and leak the loop and
    its self-pipe FDs.
    """
    worker = JobWorker(MagicMock(), _async_cb, _make_config())
    # Touch the property to spin up the loop + thread, then immediately
    # close. The startup race is most likely to fire here.
    _ = worker.worker_loop
    worker.close()
    # Loop reference cleared ⇒ no leak.
    assert worker._worker_loop is None  # pyright: ignore[reportPrivateUsage]
    assert worker._worker_thread is None  # pyright: ignore[reportPrivateUsage]
