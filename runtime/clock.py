"""The clock all SDK runtime cadence resolves through.

Worker poll loops, eventual-consistency polling, retry backoff, backpressure decay and
auth refresh all resolve time here. Pinning this pins the client's own timing, which is
what makes those loops testable without waiting for real time, and what lets a later
engine-bound implementation advance client cadence and engine time together.

See the cross-SDK contract in camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import asyncio
import threading
import time as _time
from collections.abc import Callable
from typing import Protocol, runtime_checkable

__all__ = ["Clock", "LiveClock", "ManualClock", "live_clock"]


@runtime_checkable
class Clock(Protocol):
    """Time and waiting, as the SDK runtime sees them.

    Wall-clock rather than monotonic throughout. The engine clock is wall time
    (``PUT /clock`` takes epoch milliseconds), so cadence measured on a monotonic source
    could never follow a pinned engine. :class:`LiveClock` supplies the monotonicity a
    deadline needs by other means.
    """

    def now(self) -> float:
        """Current wall-clock time in seconds since the epoch.

        Never decreases, so a deadline computed from two readings cannot be extended by a
        clock correction.
        """
        ...

    async def sleep(self, seconds: float) -> None:
        """Wait for ``seconds`` on this clock, from async code.

        An injected implementation must not return without yielding. The worker schedules
        its next poll by awaiting this, so a sleep that completes on the current step turns
        the poll loop into an unbounded spin.
        """
        ...

    def sleep_sync(self, seconds: float) -> None:
        """Wait for ``seconds`` on this clock, from blocking code.

        The sync client and thread-based job handlers need this; it is the same clock, not
        a second one, so a test that pins time drives both surfaces.
        """
        ...


#: Fraction of forward progress used to repay an absorbed backward correction: 1/16, so
#: reported time runs at 15/16 of the true rate until it has converged.
_SLEW_DIVISOR = 16.0


class LiveClock:
    """The real clock: the single place the SDK reads ambient time.

    Wall clocks move backwards — NTP correction, VM suspend and resume, a manual change —
    and a deadline computed against a backwards-moving clock waits longer than it was asked
    to. A backward step is absorbed into an offset and then repaid gradually out of forward
    progress, so readings never decrease, keep advancing immediately after a jump, and
    converge back to the underlying clock instead of staying ahead of it for good.

    Clamping to the previous high-water mark would be the simpler fix and the wrong one: it
    holds logical time still until the underlying clock catches up, so an hour-long
    correction adds an hour to every deadline in flight.

    Safe to share across threads. The default instance backs every client that does not
    inject one, and thread-based job handlers read it concurrently.
    """

    def __init__(self, source: Callable[[], float] | None = None) -> None:
        # Called through rather than captured, so a test that patches the time module still
        # drives an already-constructed clock.
        self._source = source if source is not None else (lambda: _time.time())
        # `now` is a read-modify-write over two fields; without this a concurrent reader can
        # interleave and observe -- or publish -- time that goes backwards, which is the one
        # guarantee this class exists to provide.
        self._lock = threading.Lock()
        self._last_source = self._source()
        self._offset = 0.0

    def now(self) -> float:
        with self._lock:
            observed = self._source()

            if observed < self._last_source:
                self._offset += self._last_source - observed
            elif self._offset > 0.0:
                # Float arithmetic, so there is no flooring: any forward progress repays a
                # proportional share and the offset converges. An integer-millisecond clock
                # needs a credit accumulator here; seconds-as-float does not.
                repay = (observed - self._last_source) / _SLEW_DIVISOR
                self._offset = max(0.0, self._offset - repay)

            self._last_source = observed
            return observed + self._offset

    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(max(0.0, seconds))

    def sleep_sync(self, seconds: float) -> None:
        _time.sleep(max(0.0, seconds))


#: The clock used when none is injected.
live_clock: Clock = LiveClock()


class ManualClock:
    """A deterministic clock for tests: virtual time, so poll loops and backoff settle
    without burning real time.

    Exists so nobody hand-rolls one. Every ad-hoc clock this replaces got some clause of
    the contract wrong -- most often returning from ``sleep`` without yielding, which spins
    any caller that reschedules itself on completion.

    With ``auto_advance`` (the default) a sleep moves time to its own wake point and
    returns, so the SDK's loops make progress without the test driving them: a worker that
    polls every second for a minute of virtual time finishes in real milliseconds. Set it
    to ``False`` to hold every sleep until :meth:`advance` releases it, which is what you
    want when asserting on the state *between* two waits.

    Time only ever moves forward, including when two waiters settle out of order, so the
    protocol's monotonicity clause holds however the sleeps interleave.

    ``advance`` must be called from the same thread and event loop as the sleepers it
    releases; blocking :meth:`sleep_sync` waiters in manual mode are the exception, and
    have to be released from another thread.
    """

    def __init__(self, *, start: float = 0.0, auto_advance: bool = True) -> None:
        self._now = start
        self._auto_advance = auto_advance
        # Not an RLock: nothing here needs to re-enter, and a plain lock turns any future
        # attempt to hold it across an await into a deadlock rather than silent shared-state
        # corruption.
        self._lock = threading.Lock()
        self._sleeps: list[float] = []
        self._now_calls = 0
        # Deadline plus the handle that releases it. Sync waiters carry a threading.Event,
        # async waiters an asyncio.Event, because only one of the two can be waited on from
        # each side.
        self._waiters: list[tuple[float, threading.Event | asyncio.Event]] = []

    # -- Clock -------------------------------------------------------------------

    def now(self) -> float:
        with self._lock:
            self._now_calls += 1
            return self._now

    async def sleep(self, seconds: float) -> None:
        deadline = self._register(seconds)
        event = asyncio.Event()
        with self._lock:
            already_due = self._now >= deadline
            if not already_due:
                self._waiters.append((deadline, event))

        # Every yield below is outside the lock: suspending while holding it would let
        # another coroutine on this thread observe the half-updated waiter list.
        if already_due:
            # Yield even so, because a sleep that returns on the current step is the defect
            # this clock exists to avoid.
            await asyncio.sleep(0)
            return

        if self._auto_advance:
            # Yield first, so a test observes the caller parked here before time moves.
            await asyncio.sleep(0)
            with self._lock:
                self._settle_to(deadline)

        await event.wait()

    def sleep_sync(self, seconds: float) -> None:
        deadline = self._register(seconds)
        event = threading.Event()
        with self._lock:
            if self._now >= deadline:
                return
            if self._auto_advance:
                self._settle_to(deadline)
                return
            self._waiters.append((deadline, event))

        event.wait()

    # -- Control -----------------------------------------------------------------

    async def advance(self, seconds: float) -> None:
        """Move time forward by ``seconds``, releasing every sleep that comes due, then
        let the released coroutines run before returning."""
        self.advance_sync(seconds)
        await asyncio.sleep(0)

    def advance_sync(self, seconds: float) -> None:
        """:meth:`advance` for blocking tests, which have no loop to drain.

        A negative advance raises rather than being clamped: unlike a negative sleep it
        cannot arise from an elapsed deadline, so it is a bug in the test.
        """
        if seconds < 0:
            raise ValueError(f"clock.advance needs a non-negative duration, got {seconds}")
        with self._lock:
            self._settle_to(self._now + seconds)

    def _settle_to(self, when: float) -> None:
        """Release due waiters. Caller holds the lock.

        ``max`` rather than assignment, so two waiters settling out of order cannot drag
        time backwards.
        """
        self._now = max(self._now, when)
        still_waiting = []
        for deadline, event in self._waiters:
            if deadline <= self._now:
                event.set()
            else:
                still_waiting.append((deadline, event))
        self._waiters = still_waiting

    def _register(self, seconds: float) -> float:
        # Negative durations are tolerated rather than rejected: callers compute
        # `deadline - now()`, which goes negative the moment a deadline passes.
        seconds = max(0.0, seconds)
        with self._lock:
            self._sleeps.append(seconds)
            return self._now + seconds

    # -- Introspection -----------------------------------------------------------

    @property
    def sleeps(self) -> tuple[float, ...]:
        """Durations passed to ``sleep`` and ``sleep_sync``, in call order."""
        with self._lock:
            return tuple(self._sleeps)

    @property
    def now_calls(self) -> int:
        """How many times ``now`` has been read."""
        with self._lock:
            return self._now_calls

    @property
    def pending(self) -> int:
        """Sleeps still waiting for time to advance."""
        with self._lock:
            return len(self._waiters)
