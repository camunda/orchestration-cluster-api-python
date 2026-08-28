"""Cadence runs on the injected clock.

Slice 1 gave the client a clock; on its own that changed nothing observable, because every
wait in the runtime still read ambient time. These are the tests that would have caught the
gap the JS and C# slices shipped with: the seam existed, but pinning it left the poll loops
waiting on the real clock regardless.

Each test drives a wait that nominally lasts tens of seconds and asserts it completes in
real milliseconds -- which is only possible if the wait resolved through the clock.

See camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import time as real_time

import pytest

from camunda_orchestration_sdk.runtime.backpressure import (
    AsyncBackpressureManager,
    BackpressureManager,
)
from camunda_orchestration_sdk.runtime.clock import ManualClock
from camunda_orchestration_sdk.runtime.eventual import (
    ConsistencyOptions,
    EventualConsistencyTimeoutError,
    eventual_poll,
    eventual_poll_async,
)

#: Real seconds a virtualised wait is allowed to take. Deliberately generous: it separates
#: milliseconds from the tens of seconds the virtual durations describe, so it is a safety
#: net rather than a timing assertion that could go flaky on a loaded runner.
REAL_BUDGET_S = 5.0

#: Long enough that doing it for real would be unmistakable in the test run.
VIRTUAL_WAIT_MS = 30_000


def _elapsed_since(started: float) -> float:
    return real_time.monotonic() - started


class TestEventualPollingCadence:
    """The poller's timeout and its retry gap both come from the injected clock."""

    def test_sync_timeout_elapses_without_real_waiting(self) -> None:
        clock = ManualClock(start=1_000.0)
        attempts = 0

        def never_ready() -> None:
            nonlocal attempts
            attempts += 1
            return None

        started = real_time.monotonic()
        with pytest.raises(EventualConsistencyTimeoutError):
            eventual_poll(
                "getProcessInstance",
                True,
                never_ready,
                ConsistencyOptions(wait_up_to_ms=VIRTUAL_WAIT_MS),
                None,
                clock,
            )
        elapsed = _elapsed_since(started)

        assert attempts > 1, "the poller should have retried"
        assert clock.sleeps, "the poller never slept on the injected clock"
        assert elapsed < REAL_BUDGET_S, (
            f"{VIRTUAL_WAIT_MS}ms of virtual polling burned {elapsed:.1f}s of real time -- "
            "the wait did not resolve through the injected clock"
        )

    @pytest.mark.asyncio
    async def test_async_timeout_elapses_without_real_waiting(self) -> None:
        clock = ManualClock(start=1_000.0)

        async def never_ready() -> None:
            return None

        started = real_time.monotonic()
        with pytest.raises(EventualConsistencyTimeoutError):
            await eventual_poll_async(
                "getProcessInstance",
                True,
                never_ready,
                ConsistencyOptions(wait_up_to_ms=VIRTUAL_WAIT_MS),
                None,
                clock,
            )
        elapsed = _elapsed_since(started)

        assert clock.sleeps, "the poller never slept on the injected clock"
        assert elapsed < REAL_BUDGET_S, (
            f"{VIRTUAL_WAIT_MS}ms of virtual polling burned {elapsed:.1f}s of real time"
        )

    def test_a_ready_result_is_still_returned(self) -> None:
        """Virtual time changes how long an answer takes, not what the answer is."""
        clock = ManualClock(start=1_000.0)

        result = eventual_poll(
            "getProcessInstance",
            True,
            lambda: {"ok": True},
            ConsistencyOptions(wait_up_to_ms=VIRTUAL_WAIT_MS),
            None,
            clock,
        )

        assert result == {"ok": True}
        assert not clock.sleeps, "a ready result should not have waited at all"

    def test_elapsed_time_is_measured_on_the_injected_clock(self) -> None:
        """The complement of the tests above.

        Those prove the waits cost no real time; this proves the *deadline* is the injected
        clock's. The poller reports 30s elapsed having burned none, which is only coherent
        if both the sleeping and the measuring went through the same injected clock.
        """
        clock = ManualClock(start=1_000.0)

        started = real_time.monotonic()
        with pytest.raises(EventualConsistencyTimeoutError) as caught:
            eventual_poll(
                "getProcessInstance",
                True,
                lambda: None,
                ConsistencyOptions(wait_up_to_ms=VIRTUAL_WAIT_MS),
                None,
                clock,
            )
        real_elapsed_ms = _elapsed_since(started) * 1000

        assert caught.value.elapsed_ms >= VIRTUAL_WAIT_MS, (
            "the poller gave up before its budget expired on the injected clock"
        )
        assert real_elapsed_ms < caught.value.elapsed_ms / 2, (
            f"reported {caught.value.elapsed_ms}ms elapsed but really took "
            f"{real_elapsed_ms:.0f}ms -- elapsed time was read from the ambient clock"
        )


class TestBackpressureCadence:
    """The backoff-at-floor wait, and the decay window, both resolve through the clock."""

    def test_sync_backoff_does_not_burn_real_time(self) -> None:
        clock = ManualClock(start=1_000.0)
        bp = BackpressureManager(profile="BALANCED", clock=clock)
        for _ in range(20):
            bp.record_backpressure()

        started = real_time.monotonic()
        bp.acquire()
        elapsed = _elapsed_since(started)

        assert elapsed < REAL_BUDGET_S, f"acquire burned {elapsed:.1f}s of real time"

    @pytest.mark.asyncio
    async def test_async_backoff_does_not_burn_real_time(self) -> None:
        clock = ManualClock(start=1_000.0)
        bp = AsyncBackpressureManager(profile="BALANCED", clock=clock)
        for _ in range(20):
            await bp.record_backpressure()

        started = real_time.monotonic()
        await bp.acquire()
        elapsed = _elapsed_since(started)

        assert elapsed < REAL_BUDGET_S, f"acquire burned {elapsed:.1f}s of real time"

    def test_decay_is_measured_on_the_injected_clock(self) -> None:
        clock = ManualClock(start=1_000.0, auto_advance=False)
        bp = BackpressureManager(profile="BALANCED", clock=clock)

        before = clock.now_calls
        bp.record_backpressure()

        assert clock.now_calls > before, (
            "the decay window must be measured on the injected clock"
        )
