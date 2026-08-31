"""The engine-bound clock, and the incident it closes.

Slice 5, and the reason the previous four exist. The motivating failure was a worker that
busy-polled for a real minute while the engine's clock was pinned: the seam existed, a test
clock existed, and the two clocks still had nothing to do with each other.

`EngineClock` is what joins them. Every wait pins the engine forward by exactly the interval
the caller asked to wait, so client cadence and engine time advance together. The headline
test below is the incident, inverted: a worker polling for something that never becomes
ready, across a minute of engine time, finishing in real milliseconds.

`PUT /clock` is write-only, so the fake target here is also the only way to observe what was
pinned -- there is no endpoint to read it back from.

See camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import asyncio
import threading
import time as real_time
from collections.abc import Callable

import pytest

from camunda_orchestration_sdk.runtime.clock import Clock, EngineClock

#: Real seconds a virtualised wait may take. A safety net, not a timing assertion.
REAL_BUDGET_S = 5.0

#: The engine time the headline test spans. A minute of real polling would be unmistakable.
ENGINE_MINUTE_S = 60.0


class FakeEngine:
    """The `PUT /clock` half of the client, and the only way to see what was pinned.

    ``pin_clock`` yields before recording. That one ``await`` is the difference between a
    double that models an HTTP client and one that does not: without it a pin completes
    within a single step, no other task can ever interleave, and a serialisation test passes
    because there is nothing to serialise. That is precisely how the concurrency defect this
    class now guards against got past review.
    """

    def __init__(self) -> None:
        self.pins: list[int] = []
        self.resets = 0

    async def pin_clock(self, *, data, **kwargs) -> None:
        await asyncio.sleep(0)
        self.pins.append(data.timestamp)

    async def reset_clock(self, **kwargs) -> None:
        await asyncio.sleep(0)
        self.resets += 1


class SyncFakeEngine:
    def __init__(self) -> None:
        self.pins: list[int] = []
        self.resets = 0

    def pin_clock(self, *, data, **kwargs) -> None:
        self.pins.append(data.timestamp)

    def reset_clock(self, **kwargs) -> None:
        self.resets += 1


class BlockingEngine:
    """A pin the test can hold open, so a second caller can be observed arriving mid-pin."""

    def __init__(self) -> None:
        self.pins: list[int] = []
        self.pin_started = asyncio.Event()
        self.release = asyncio.Event()

    async def pin_clock(self, *, data, **kwargs) -> None:
        self.pin_started.set()
        await self.release.wait()
        self.pins.append(data.timestamp)

    async def reset_clock(self, **kwargs) -> None: ...


def _raises_off_thread(call: Callable[[], None], timeout: float = 5.0) -> str:
    """Run a blocking call on a worker thread and return the message it raised.

    The regressions these guard are deadlocks, so running them inline would wedge the suite
    rather than fail it. Returns "" if nothing was raised, and fails on the timeout.
    """
    raised: list[BaseException] = []
    finished = threading.Event()

    def run() -> None:
        try:
            call()
        except BaseException as exc:
            raised.append(exc)
        finally:
            finished.set()

    threading.Thread(target=run, daemon=True).start()

    assert finished.wait(timeout=timeout), (
        "the call deadlocked instead of returning; the guard did not fire"
    )
    if not raised:
        return ""
    message = str(raised[0])
    return "re-entered while pinning" if "re-entered while pinning" in message else message


class TestWaitingAdvancesTheEngine:
    @pytest.mark.asyncio
    async def test_a_wait_pins_the_engine_forward_by_the_interval(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await clock.sleep(30.0)

        assert clock.now() == 1_030.0
        assert engine.pins == [1_030_000], "the engine was not moved to the new time"

    @pytest.mark.asyncio
    async def test_a_wait_costs_no_real_time(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        started = real_time.monotonic()
        await clock.sleep(ENGINE_MINUTE_S)
        elapsed = real_time.monotonic() - started

        assert elapsed < REAL_BUDGET_S, f"waiting a virtual minute took {elapsed:.1f}s"

    @pytest.mark.asyncio
    async def test_overlapping_waits_settle_at_one_wake_instant(self) -> None:
        """Twenty handlers each waiting a second is one second of engine time, not twenty.

        Resolving the target inside the lock would sum them, so engine time would run faster
        the more concurrent the worker is -- and a pinned engine would race ahead of the
        process it is supposed to be driving.
        """
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await asyncio.gather(*(clock.sleep(1.0) for _ in range(20)))

        assert clock.now() == 1_001.0, "overlapping waits accumulated instead of settling"
        assert engine.pins == sorted(engine.pins), f"engine time went backwards: {engine.pins}"
        assert engine.pins[-1] == 1_001_000

    @pytest.mark.asyncio
    async def test_sequential_waits_still_compose(self) -> None:
        """The complement: waits that do not overlap must each move time on."""
        clock = EngineClock(FakeEngine(), start=1_000.0)

        for _ in range(3):
            await clock.sleep(1.0)

        assert clock.now() == 1_003.0

    @pytest.mark.asyncio
    async def test_a_rejected_pin_leaves_the_clock_where_it_was(self) -> None:
        """Publishing before the engine accepts would build later waits on a time it never
        adopted."""

        class RefusingEngine:
            async def pin_clock(self, *, data, **kwargs) -> None:
                raise RuntimeError("503 from the engine")

            async def reset_clock(self, **kwargs) -> None: ...

        clock = EngineClock(RefusingEngine(), start=1_000.0)

        with pytest.raises(RuntimeError, match="503"):
            await clock.sleep(30.0)

        assert clock.now() == 1_000.0, "the clock advanced despite the engine refusing"

    @pytest.mark.asyncio
    async def test_concurrent_waits_queue_rather_than_being_rejected(self) -> None:
        """Ordinary concurrency is not re-entry.

        A single "someone is pinning" flag cannot tell the two apart, and rejects the second
        caller the moment a pin awaits real I/O -- which makes the clock unusable under the
        concurrency a worker normally has.

        The second wait has to *arrive while the first is mid-pin* for this to test
        anything. A plain ``gather`` does not: every task clears the guard on the first step,
        before any of them has started pinning, so it passes either way.
        """
        engine = BlockingEngine()
        clock = EngineClock(engine, start=1_000.0)

        first = asyncio.ensure_future(clock.sleep(1.0))
        await asyncio.wait_for(engine.pin_started.wait(), timeout=5.0)

        second = asyncio.ensure_future(clock.sleep(1.0))
        await asyncio.sleep(0)  # let it reach the guard while `first` is still pinning

        engine.release.set()
        outcomes = await asyncio.wait_for(
            asyncio.gather(first, second, return_exceptions=True), timeout=5.0
        )

        raised = [o for o in outcomes if isinstance(o, BaseException)]
        assert not raised, f"a wait arriving mid-pin was rejected as re-entry: {raised}"
        assert len(engine.pins) == 2, "the queued wait never reached the engine"

    @pytest.mark.asyncio
    async def test_a_wait_yields_to_the_event_loop(self) -> None:
        """The Clock clause hand-rolled implementations break most often: a sleep that returns
        on the current step turns a caller that reschedules itself into a spin."""
        clock = EngineClock(FakeEngine(), start=1_000.0)
        settled = False

        async def waiter() -> None:
            nonlocal settled
            await clock.sleep(1.0)
            settled = True

        task = asyncio.ensure_future(waiter())
        await asyncio.sleep(0)
        assert not settled, "sleep() completed without yielding"

        await asyncio.wait_for(task, timeout=5.0)
        assert settled

    def test_a_sync_client_advances_it_too(self) -> None:
        engine = SyncFakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        clock.sleep_sync(30.0)

        assert clock.now() == 1_030.0
        assert engine.pins == [1_030_000]


class TestControl:
    @pytest.mark.asyncio
    async def test_pin_sets_an_explicit_time(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await clock.pin(2_000.0)

        assert clock.now() == 2_000.0
        assert engine.pins == [2_000_000]

    @pytest.mark.asyncio
    async def test_pin_without_an_argument_pins_where_the_clock_already_is(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await clock.pin()

        assert engine.pins == [1_000_000]

    @pytest.mark.asyncio
    async def test_reset_hands_the_engine_back_to_real_time(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await clock.reset()

        assert engine.resets == 1
        assert clock.now() > 1_000.0, "after a reset the clock should follow real time again"

    @pytest.mark.asyncio
    async def test_after_a_reset_the_clock_keeps_ticking(self) -> None:
        """Storing one wall-clock reading would leave it stopped, not following."""
        clock = EngineClock(FakeEngine(), start=1_000.0)

        await clock.reset()
        first = clock.now()
        await asyncio.sleep(0.02)
        second = clock.now()

        assert second > first, "the clock froze at a single reading instead of following"

    def test_it_starts_at_real_time_by_default(self) -> None:
        """Defaulting to the epoch would pin a live engine to 1970, and with it every date
        in every process running on that engine."""
        clock = EngineClock(FakeEngine())

        assert clock.now() > 1_700_000_000.0, "an engine clock must not start at the epoch"

    def test_the_direction_can_be_stated_rather_than_inferred(self) -> None:
        """Inference reads `def pin_clock(...) -> Awaitable[None]` as synchronous, though the
        target protocol allows it."""

        class DecoratedEngine:
            def pin_clock(self, *, data, **kwargs):
                async def issue() -> None: ...

                return issue()

            def reset_clock(self, **kwargs):
                async def issue() -> None: ...

                return issue()

        inferred = EngineClock(DecoratedEngine(), start=1_000.0)
        assert inferred._is_async is False  # pyright: ignore[reportPrivateUsage]

        stated = EngineClock(DecoratedEngine(), start=1_000.0, is_async=True)
        assert stated._is_async is True  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_timestamps_are_epoch_milliseconds(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_700_000_000.0)

        await clock.pin()

        assert engine.pins == [1_700_000_000_000]


class TestItRefusesToDriveItsOwnClient:
    """Pinning issues a request, and that request's own backoff waits on a clock. If that is
    this clock, the pin waits on itself."""

    def test_a_self_referential_target_is_rejected_at_construction(self) -> None:
        class ClientHoldingItsOwnClock:
            def __init__(self) -> None:
                self.clock: Clock | None = None

            async def pin_clock(self, *, data, **kwargs) -> None: ...

            async def reset_clock(self, **kwargs) -> None: ...

        client = ClientHoldingItsOwnClock()
        clock = EngineClock(client, start=1_000.0)
        client.clock = clock

        with pytest.raises(ValueError, match="cannot drive the client it is injected into"):
            EngineClock.__init__(clock, client, start=1_000.0)

    @pytest.mark.asyncio
    async def test_re_entering_while_pinning_raises_rather_than_recursing(self) -> None:
        """The failure that survives construction: a target wired up after the fact. Better
        a loud error than a stack overflow or a hang."""
        holder: dict[str, EngineClock] = {}

        class ReentrantEngine:
            async def pin_clock(self, *, data, **kwargs) -> None:
                await holder["clock"].sleep(1.0)

            async def reset_clock(self, **kwargs) -> None: ...

        clock = EngineClock(ReentrantEngine(), start=1_000.0)
        holder["clock"] = clock

        with pytest.raises(RuntimeError, match="re-entered while pinning"):
            await clock.sleep(1.0)

    def test_the_same_check_holds_on_the_synchronous_path(self) -> None:
        """Run on a worker thread with a timeout, because the regression this guards is a
        deadlock: asserting it inline would wedge the suite instead of failing it.

        The sync owner is a thread id, and `threading.get_ident()` returns an int too large
        for CPython's small-int cache -- so two calls on one thread are equal without being
        the same object, and an identity check silently lets re-entry through.
        """
        holder: dict[str, EngineClock] = {}

        class ReentrantSyncEngine:
            def pin_clock(self, *, data, **kwargs) -> None:
                holder["clock"].sleep_sync(1.0)

            def reset_clock(self, **kwargs) -> None: ...

        clock = EngineClock(ReentrantSyncEngine(), start=1_000.0)
        holder["clock"] = clock

        assert _raises_off_thread(lambda: clock.sleep_sync(1.0)) == "re-entered while pinning"

    @pytest.mark.asyncio
    async def test_reset_is_guarded_too(self) -> None:
        """`reset` issues a request just as `pin` does, so it needs to record the owner too.
        Without it the guard sees nobody pinning and the re-entrant call waits forever on the
        lock the outer reset is holding."""
        holder: dict[str, EngineClock] = {}

        class ReentrantResetEngine:
            async def pin_clock(self, *, data, **kwargs) -> None: ...

            async def reset_clock(self, **kwargs) -> None:
                await holder["clock"].sleep(1.0)

        clock = EngineClock(ReentrantResetEngine(), start=1_000.0)
        holder["clock"] = clock

        with pytest.raises(RuntimeError, match="re-entered while pinning"):
            await asyncio.wait_for(clock.reset(), timeout=5.0)

    def test_the_synchronous_reset_is_guarded_too(self) -> None:
        holder: dict[str, EngineClock] = {}

        class ReentrantSyncResetEngine:
            def pin_clock(self, *, data, **kwargs) -> None: ...

            def reset_clock(self, **kwargs) -> None:
                holder["clock"].sleep_sync(1.0)

        clock = EngineClock(ReentrantSyncResetEngine(), start=1_000.0)
        holder["clock"] = clock

        assert _raises_off_thread(clock.reset_sync) == "re-entered while pinning"


class TestTheWrongDirectionFailsLoudly:
    @pytest.mark.asyncio
    async def test_a_blocking_wait_on_an_async_client_is_refused(self) -> None:
        clock = EngineClock(FakeEngine(), start=1_000.0)

        with pytest.raises(RuntimeError, match="asynchronous client"):
            clock.sleep_sync(1.0)

    @pytest.mark.asyncio
    async def test_an_awaited_wait_on_a_sync_client_is_refused(self) -> None:
        """Rather than blocking the event loop on an HTTP round trip."""
        clock = EngineClock(SyncFakeEngine(), start=1_000.0)

        with pytest.raises(RuntimeError, match="synchronous client"):
            await clock.sleep(1.0)

    @pytest.mark.asyncio
    async def test_an_awaited_pin_on_a_sync_client_is_refused(self) -> None:
        """`pin` and `reset` need the same gate as `sleep`: awaiting a sync client would run
        a blocking request on the loop, and calling an async one without awaiting would drop
        the request silently."""
        clock = EngineClock(SyncFakeEngine(), start=1_000.0)

        with pytest.raises(RuntimeError, match="synchronous client"):
            await clock.pin(2_000.0)
        with pytest.raises(RuntimeError, match="synchronous client"):
            await clock.reset()

    def test_a_blocking_pin_on_an_async_client_is_refused(self) -> None:
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        with pytest.raises(RuntimeError, match="asynchronous client"):
            clock.pin_sync(2_000.0)
        with pytest.raises(RuntimeError, match="asynchronous client"):
            clock.reset_sync()

        assert engine.pins == [] and engine.resets == 0, (
            "the request must not have been issued and dropped"
        )


def test_it_satisfies_the_clock_protocol() -> None:
    assert isinstance(EngineClock(FakeEngine()), Clock)
