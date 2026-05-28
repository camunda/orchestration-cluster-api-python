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


def test_job_worker_concurrent_close_is_idempotent() -> None:
    """Two threads calling close() concurrently must not both try to
    tear down the worker loop. Without an atomic teardown claim, both
    would call self._worker_loop.close() and one would either raise or
    leak the self-pipe FDs.
    """
    import threading as _threading

    worker = JobWorker(MagicMock(), _async_cb, _make_config())
    # Force loop + pool allocation so close() has real work to do.
    _ = worker.worker_loop
    _ = worker.thread_pool

    barrier = _threading.Barrier(4)
    errors: list[BaseException] = []

    def race() -> None:
        try:
            barrier.wait(timeout=5.0)
            worker.close()
        except BaseException as e:  # noqa: BLE001 — propagate any race fallout
            errors.append(e)

    threads = [_threading.Thread(target=race) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10.0)
        assert not t.is_alive(), "close() race left a thread hanging"

    assert errors == [], f"Concurrent close() raised: {errors!r}"
    assert worker._worker_loop is None  # pyright: ignore[reportPrivateUsage]
    assert worker._thread_pool is None  # pyright: ignore[reportPrivateUsage]


def test_job_worker_property_access_after_close_raises() -> None:
    """Lazy properties must refuse to allocate new resources after close().

    Without this guard, a close() racing a property access can shut
    down the old pool a microsecond before the property creates a brand-
    new one — silently leaking the new pool.
    """
    worker = JobWorker(MagicMock(), _sync_cb, _make_config())
    worker.close()
    with pytest.raises(RuntimeError, match="closed"):
        _ = worker.thread_pool
    with pytest.raises(RuntimeError, match="closed"):
        _ = worker.process_pool
    with pytest.raises(RuntimeError, match="closed"):
        _ = worker.worker_loop


def test_get_sync_client_is_lazy_and_one_shot_under_concurrency() -> None:
    """_get_sync_client must not create two clients under concurrent access.

    Same defect class as the thread/process pool lazy init the reviewer
    flagged. Without locking, two _execute_job calls in the thread
    strategy can both observe None and both construct a CamundaClient,
    leaking the overwritten one along with its httpx connection pool.
    """
    import threading as _threading

    worker = JobWorker(MagicMock(), _sync_cb, _make_config())
    barrier = _threading.Barrier(8)
    clients: list[Any] = []

    def race() -> None:
        barrier.wait(timeout=5.0)
        clients.append(worker._get_sync_client())  # pyright: ignore[reportPrivateUsage]

    threads = [_threading.Thread(target=race) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10.0)

    # All callers must receive the *same* instance — proof there was no
    # leaked overwritten one.
    assert len(clients) == 8
    first = clients[0]
    assert all(c is first for c in clients), (
        "concurrent _get_sync_client() created multiple instances"
    )
    worker.close()


def test_close_from_worker_loop_thread_does_not_self_join() -> None:
    """close() invoked from the worker_loop thread must skip joining it.

    Mirror of the pool self-join hazard. If an async callback running
    on worker_loop calls worker.close(), the join would target the
    current thread and raise RuntimeError ('cannot join current thread').
    """
    import asyncio as _asyncio

    worker = JobWorker(MagicMock(), _async_cb, _make_config())
    loop = worker.worker_loop  # allocate
    # Wait for the loop to actually be running before we schedule.
    worker._worker_loop_started.wait(timeout=2.0)  # pyright: ignore[reportPrivateUsage]

    done = _asyncio.run_coroutine_threadsafe(_close_from_within(worker), loop)
    # Generous timeout: a real deadlock would hang here; a self-join
    # RuntimeError would surface as a future exception.
    done.result(timeout=5.0)


async def _close_from_within(worker: JobWorker) -> None:
    worker.close()
