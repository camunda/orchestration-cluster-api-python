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
import time as real_time

import pytest

from camunda_orchestration_sdk.runtime.clock import Clock, EngineClock

#: Real seconds a virtualised wait may take. A safety net, not a timing assertion.
REAL_BUDGET_S = 5.0

#: The engine time the headline test spans. A minute of real polling would be unmistakable.
ENGINE_MINUTE_S = 60.0


class FakeEngine:
    """The `PUT /clock` half of the client, and the only way to see what was pinned."""

    def __init__(self) -> None:
        self.pins: list[int] = []
        self.resets = 0

    async def pin_clock(self, *, data, **kwargs) -> None:
        self.pins.append(data.timestamp)

    async def reset_clock(self, **kwargs) -> None:
        self.resets += 1


class SyncFakeEngine:
    def __init__(self) -> None:
        self.pins: list[int] = []
        self.resets = 0

    def pin_clock(self, *, data, **kwargs) -> None:
        self.pins.append(data.timestamp)

    def reset_clock(self, **kwargs) -> None:
        self.resets += 1


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
    async def test_engine_time_only_moves_forward(self) -> None:
        """Concurrent waits computing from one reading would collapse into a single advance,
        and the pin that lost the race would drag the engine backwards."""
        engine = FakeEngine()
        clock = EngineClock(engine, start=1_000.0)

        await asyncio.gather(*(clock.sleep(1.0) for _ in range(20)))

        assert engine.pins == sorted(engine.pins), f"engine time went backwards: {engine.pins}"
        assert len(engine.pins) == 20, "an advance was lost to a race"
        assert clock.now() == 1_020.0

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

    def test_it_starts_at_real_time_by_default(self) -> None:
        """Defaulting to the epoch would pin a live engine to 1970, and with it every date
        in every process running on that engine."""
        clock = EngineClock(FakeEngine())

        assert clock.now() > 1_700_000_000.0, "an engine clock must not start at the epoch"

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


def test_it_satisfies_the_clock_protocol() -> None:
    assert isinstance(EngineClock(FakeEngine()), Clock)
