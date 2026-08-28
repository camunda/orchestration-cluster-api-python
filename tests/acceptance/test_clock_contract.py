"""Runs the `Clock` contract against every implementation, plus LiveClock's own behaviour."""

from __future__ import annotations

import asyncio
import threading
import time

import pytest

from camunda_orchestration_sdk.runtime.clock import Clock, LiveClock, ManualClock, live_clock
from camunda_orchestration_sdk.runtime.configuration_resolver import CamundaSdkConfigPartial
from clock_contract import CONTRACT, ClockSubject


def _live_subject() -> ClockSubject:
    return ClockSubject(
        name="LiveClock",
        clock=LiveClock(),
        advance=asyncio.sleep,
    )


def _manual_subject() -> ClockSubject:
    clock = ManualClock(start=1_000.0)
    return ClockSubject(
        name="ManualClock",
        clock=clock,
        advance=clock.advance,
    )


#: Add an implementation here and it inherits the whole contract.
SUBJECT_FACTORIES = {
    "LiveClock": _live_subject,
    "ManualClock": _manual_subject,
}


@pytest.mark.parametrize("factory_name", sorted(SUBJECT_FACTORIES))
@pytest.mark.parametrize("clause", CONTRACT, ids=lambda c: c.__name__)
@pytest.mark.asyncio
async def test_clock_contract(factory_name: str, clause) -> None:
    await clause(SUBJECT_FACTORIES[factory_name]())


class TestManualClock:
    """Manual mode: the behaviour the contract, which runs auto-advance, cannot reach."""

    @pytest.mark.asyncio
    async def test_a_sleep_is_held_until_time_advances(self) -> None:
        clock = ManualClock(start=1_000.0, auto_advance=False)
        settled = False

        async def waiter() -> None:
            nonlocal settled
            await clock.sleep(30.0)
            settled = True

        task = asyncio.ensure_future(waiter())
        await asyncio.sleep(0)
        assert not settled and clock.pending == 1

        await clock.advance(29.0)
        assert not settled, "a partial advance must not release the sleep"

        await clock.advance(1.0)
        await asyncio.wait_for(task, timeout=5.0)
        assert settled and clock.pending == 0

    @pytest.mark.asyncio
    async def test_out_of_order_settlement_cannot_move_time_backwards(self) -> None:
        clock = ManualClock(start=1_000.0, auto_advance=False)
        await clock.advance(50.0)
        clock.advance_sync(0.0)

        assert clock.now() == 1_050.0

    def test_a_blocking_sleep_is_released_from_another_thread(self) -> None:
        clock = ManualClock(start=1_000.0, auto_advance=False)
        released = threading.Event()

        def sleeper() -> None:
            clock.sleep_sync(30.0)
            released.set()

        thread = threading.Thread(target=sleeper, daemon=True)
        thread.start()
        assert not released.wait(timeout=0.1), "sleep_sync returned before time advanced"

        clock.advance_sync(30.0)
        assert released.wait(timeout=5.0), "sleep_sync was never released"
        thread.join(timeout=5.0)

    @pytest.mark.asyncio
    async def test_auto_advance_settles_a_long_sleep_without_real_waiting(self) -> None:
        """The property the whole slice rests on: virtual duration, real immediacy."""
        clock = ManualClock(start=1_000.0)

        started = time.monotonic()
        await clock.sleep(600.0)
        real_elapsed = time.monotonic() - started

        assert clock.now() == 1_600.0
        assert real_elapsed < 5.0, f"a virtual sleep took {real_elapsed:.1f}s of real time"

    def test_advance_rejects_a_negative_duration(self) -> None:
        """Unlike a sleep, this cannot come from an elapsed deadline -- so it is a bug."""
        with pytest.raises(ValueError):
            ManualClock().advance_sync(-1.0)

    def test_it_records_what_was_asked_of_it(self) -> None:
        clock = ManualClock(start=1_000.0)
        clock.sleep_sync(1.5)
        clock.sleep_sync(2.5)

        assert clock.sleeps == (1.5, 2.5)


class TestLiveClockSlew:
    """The behaviour the contract cannot express: what happens when the source jumps."""

    def test_absorbs_a_backward_jump_instead_of_reporting_it(self) -> None:
        source = [1_000.0]
        clock = LiveClock(source=lambda: source[0])

        first = clock.now()
        source[0] = 900.0  # the wall clock jumps back 100s
        second = clock.now()

        assert second >= first, "a backward jump must not be visible to callers"

    def test_keeps_advancing_immediately_after_a_backward_jump(self) -> None:
        """Clamping to the high-water mark would freeze here, adding the whole correction
        to every deadline in flight."""
        source = [1_000.0]
        clock = LiveClock(source=lambda: source[0])

        clock.now()
        source[0] = 900.0
        after_jump = clock.now()

        source[0] = 910.0  # 10s of real progress
        assert clock.now() > after_jump, "time must keep moving after a correction"

    def test_converges_back_to_the_source(self) -> None:
        """The offset is repaid out of forward progress rather than carried for ever."""
        source = [1_000.0]
        clock = LiveClock(source=lambda: source[0])

        clock.now()
        source[0] = 999.0  # absorb a 1s backward step
        clock.now()

        # Enough forward progress to repay it many times over.
        for _ in range(200):
            source[0] += 1.0
            clock.now()

        assert clock.now() == pytest.approx(source[0], abs=0.01), (
            "reported time should converge back to the underlying clock"
        )

    def test_reads_the_source_through_a_call(self) -> None:
        """Capturing the function instead of calling through it would make a clock
        constructed before a patch invisible to that patch."""
        source = [1_000.0]
        clock = LiveClock(source=lambda: source[0])

        clock.now()
        source[0] = 2_000.0

        assert clock.now() == pytest.approx(2_000.0)

    def test_serialises_the_read_modify_write(self) -> None:
        """`now` reads and then writes `_last_source` and `_offset`. Thread-based job
        handlers share a clock, so two callers inside that window can lose an offset update
        and let a caller watch its own time go backwards.

        Asserting on emitted values would be a probabilistic test of a race. This asserts
        the property that removes the race: only one thread is ever inside the critical
        section.
        """
        in_flight = 0
        peak = 0

        def watched_source() -> float:
            nonlocal in_flight, peak
            in_flight += 1
            peak = max(peak, in_flight)
            time.sleep(0.001)  # widen the window so an unguarded overlap is certain
            in_flight -= 1
            return 1_000.0

        clock = LiveClock(source=watched_source)

        threads = [
            threading.Thread(target=lambda: [clock.now() for _ in range(5)])
            for _ in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert peak == 1, f"{peak} threads were inside now() at once; the update is not atomic"


def test_live_clock_is_a_clock() -> None:
    assert isinstance(live_clock, Clock)
    assert isinstance(LiveClock(), Clock)


class TestClientInjection:
    """The seam is worth nothing if the clients do not accept it."""

    @staticmethod
    def _config() -> CamundaSdkConfigPartial:
        return {
            "CAMUNDA_REST_ADDRESS": "http://example:8080/v2",
            "CAMUNDA_AUTH_STRATEGY": "NONE",
        }

    def test_sync_client_defaults_to_the_live_clock(self) -> None:
        from camunda_orchestration_sdk import CamundaClient

        assert CamundaClient(configuration=self._config()).clock is live_clock

    def test_async_client_defaults_to_the_live_clock(self) -> None:
        from camunda_orchestration_sdk import CamundaAsyncClient

        assert CamundaAsyncClient(configuration=self._config()).clock is live_clock

    def test_sync_client_exposes_the_injected_clock(self) -> None:
        from camunda_orchestration_sdk import CamundaClient

        injected = LiveClock()
        assert CamundaClient(configuration=self._config(), clock=injected).clock is injected

    def test_async_client_exposes_the_injected_clock(self) -> None:
        from camunda_orchestration_sdk import CamundaAsyncClient

        injected = LiveClock()
        client = CamundaAsyncClient(configuration=self._config(), clock=injected)
        assert client.clock is injected
