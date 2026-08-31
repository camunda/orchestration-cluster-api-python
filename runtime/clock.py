"""The clock all SDK runtime cadence resolves through.

Worker poll loops, eventual-consistency polling, retry backoff, backpressure decay and
auth refresh all resolve time here. Pinning this pins the client's own timing, which is
what makes those loops testable without waiting for real time, and what lets
:class:`EngineClock` advance client cadence and engine time together.

See the cross-SDK contract in camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import asyncio
import inspect
import threading
import time as _time
from collections.abc import Awaitable, Callable, Coroutine
from typing import Protocol, runtime_checkable

from camunda_orchestration_sdk.models.clock_pin_request import ClockPinRequest

__all__ = [
    "Clock",
    "EngineClock",
    "EngineClockTarget",
    "LiveClock",
    "ManualClock",
    "live_clock",
]


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
        self._source = source if source is not None else (lambda: _time.time())  # noqa: TID251 — the live clock is the one place ambient time belongs
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
        await asyncio.sleep(max(0.0, seconds))  # noqa: TID251 — real waiting is what a live clock does

    def sleep_sync(self, seconds: float) -> None:
        _time.sleep(max(0.0, seconds))  # noqa: TID251 — real waiting is what a live clock does


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
            await asyncio.sleep(0)  # noqa: TID251 — a zero delay yields to the loop; it consumes no time
            return

        if self._auto_advance:
            # Yield first, so a test observes the caller parked here before time moves.
            await asyncio.sleep(0)  # noqa: TID251 — a zero delay yields to the loop; it consumes no time
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
        await asyncio.sleep(0)  # noqa: TID251 — a zero delay yields to the loop; it consumes no time

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


@runtime_checkable
class EngineClockTarget(Protocol):
    """The slice of the client :class:`EngineClock` drives.

    Narrower than the client on purpose: it is the whole surface, so a test double is a few
    lines and the coupling is visible.
    """

    def pin_clock(self, *, data: ClockPinRequest) -> Awaitable[None] | None: ...

    def reset_clock(self) -> Awaitable[None] | None: ...


class EngineClock:
    """A clock bound to the engine's own clock, so client cadence and engine time move
    together.

    This is the point of the whole contract. A worker waiting on a process that only
    completes after a BPMN timer fires has two clocks to satisfy: its own poll interval, and
    the engine's. Pin only the engine and the worker keeps waiting on real time; drive only
    the client and the engine never reaches the timer. Every wait here does both -- the
    engine is pinned forward by exactly the interval the caller asked to wait -- so a process
    spanning a minute of engine time finishes in real milliseconds.

    ``PUT /clock`` is write-only: there is no way to read the engine's time back. So this
    tracks what it last pinned, and that mirror is only accurate while nothing else pins the
    same engine. One clock per engine.

    Waits settle at a wake instant, they do not accumulate. A wait fixes its wake instant
    when it is scheduled and the engine is moved to the latest one, so ten handlers each
    waiting a second advance the engine by a second -- as real sleeps would. Summing them
    instead would make engine time run faster the more concurrent the worker is.

    Local time is published only after the engine accepts the pin. A failed request leaves
    the mirror where it was rather than ahead of a time the engine never adopted.

    Point it at a *different* client from the one it is injected into, and put the engine
    back before you finish::

        engine = EngineClock(admin_client)
        await engine.pin()
        try:
            client = CamundaAsyncClient(clock=engine)
            ...
        finally:
            await client.aclose()   # stop everything that waits on this clock first
            await engine.reset()

    .. warning::
       Pinning stops time for **everything on that cluster**, not just this client. Use it
       only against a cluster you own -- a local one, or a disposable test instance -- and
       never against a shared or production environment. Leaving without ``reset()`` leaves
       the engine frozen for whoever comes next, so the reset belongs in a ``finally``,
       after the client and any workers using the clock have stopped.

    A client whose own cadence resolves through this clock cannot be its target: pinning
    would issue a request whose backoff waits on the clock issuing it.

    ``pin(at)`` and ``reset()`` are control operations and may move time backwards -- an
    explicit, requested discontinuity. Waits never do.
    """

    def __init__(
        self,
        target: EngineClockTarget,
        *,
        start: float | None = None,
        is_async: bool | None = None,
    ) -> None:
        if getattr(target, "clock", None) is self:
            raise ValueError(
                "EngineClock cannot drive the client it is injected into: pinning would "
                "issue a request whose own cadence waits on this clock. Point it at a "
                "separate client."
            )
        self._target = target
        # Inferred, because the async and sync clients differ only in this. The override
        # exists because the inference is narrower than the protocol: a target may satisfy
        # `EngineClockTarget` with a plain `def` returning an awaitable (a decorator, say),
        # which introspection reads as synchronous.
        self._is_async = (
            is_async if is_async is not None else inspect.iscoroutinefunction(target.pin_clock)
        )
        # Until something is pinned there is nothing to mirror, so follow real time. A
        # `start` of 0 would otherwise pin a live engine to 1970, and with it every date in
        # every process running on that engine.
        self._now = start if start is not None else 0.0
        self._pinned = start is not None
        self._state_lock = threading.Lock()
        self._sync_lock = threading.Lock()
        self._async_lock: asyncio.Lock | None = None
        # The loop an async-bound clock belongs to, captured on first use. Thread-strategy
        # handlers run off-loop and still have to reach the engine, so their blocking calls
        # are bridged onto it.
        self._loop: asyncio.AbstractEventLoop | None = None
        self._loop_thread: int | None = None
        # Who is mid-request, not merely whether someone is. A bare flag cannot tell a caller
        # re-entering its own pin from an unrelated task queueing behind it, and would
        # reject the second -- which is ordinary concurrency, not misuse.
        self._pin_owner: object | None = None

    # -- Clock -------------------------------------------------------------------

    def now(self) -> float:
        with self._state_lock:
            return self._now if self._pinned else live_clock.now()

    async def sleep(self, seconds: float) -> None:
        """Advance the engine to this wait's wake instant instead of waiting it out."""
        self._require_async("sleep")
        self._guard_reentry()
        # Fixed before queueing: overlapping waits share a wake instant rather than each
        # adding its own interval on top of whoever went first.
        deadline = self._wake_instant(seconds)
        # The Clock contract requires a sleep to yield. Pinning normally awaits I/O, but that
        # is the target's business, not a guarantee -- and a sleep that returns on the
        # current step turns a poll loop into a spin.
        await asyncio.sleep(0)  # noqa: TID251 — a zero delay yields to the loop; it consumes no time
        async with self._acquire_async():
            await self._pin_async(max(self.now(), deadline))

    def sleep_sync(self, seconds: float) -> None:
        """Advance the engine to this wait's wake instant instead of waiting it out.

        Safe to call from a thread-strategy handler: an async-bound clock hands the pin to
        its own loop and blocks this thread until the engine has taken it.
        """
        if self._is_async:
            self._bridge(self.sleep(seconds), "sleep")
            return
        self._guard_reentry()
        deadline = self._wake_instant(seconds)
        with self._sync_lock:
            self._pin_sync(max(self.now(), deadline))

    # -- Control -----------------------------------------------------------------

    async def pin(self, at: float | None = None) -> None:
        """Pin the engine to ``at`` (default: this clock's current time)."""
        self._require_async("pin")
        self._guard_reentry()
        async with self._acquire_async():
            await self._pin_async(at if at is not None else self.now())

    def pin_sync(self, at: float | None = None) -> None:
        if self._is_async:
            self._bridge(self.pin(at), "pin")
            return
        self._guard_reentry()
        with self._sync_lock:
            self._pin_sync(at if at is not None else self.now())

    async def reset(self) -> None:
        """Hand the engine back to real time, and follow it again."""
        self._require_async("reset")
        self._guard_reentry()
        async with self._acquire_async():
            self._pin_owner = self._current_owner()
            try:
                await self._call(self._target.reset_clock())
            finally:
                self._pin_owner = None
            self._unpin()

    def reset_sync(self) -> None:
        if self._is_async:
            self._bridge(self.reset(), "reset")
            return
        self._guard_reentry()
        with self._sync_lock:
            self._pin_owner = self._current_owner()
            try:
                self._target.reset_clock()
            finally:
                self._pin_owner = None
            self._unpin()

    # -- Internals ---------------------------------------------------------------

    def _acquire_async(self) -> asyncio.Lock:
        # Built on first use: a lock created before the loop exists binds to the wrong one.
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
            self._loop_thread = threading.get_ident()
        return self._async_lock

    def _bridge(self, coro: Coroutine[object, object, None], what: str) -> None:
        """Run an async operation from a blocking caller on the loop that owns this clock.

        The worker's own poll loop awaits, so a clock driving a worker is always async-bound;
        but a sync handler runs on a pool thread and is documented to call ``sleep_sync``.
        Rejecting it there would leave the default strategy for sync callbacks unable to use
        an engine clock at all.
        """
        loop = self._loop
        if loop is None or loop.is_closed() or not loop.is_running():
            coro.close()
            raise RuntimeError(
                f"This EngineClock is bound to an asynchronous client and no running loop "
                f"has used it yet, so clock.{what}_sync() cannot reach the engine. Await it "
                f"once (`await clock.pin()`) before handing it to blocking callers."
            )
        if threading.get_ident() == self._loop_thread:
            coro.close()
            raise RuntimeError(
                f"clock.{what}_sync() was called on the event loop's own thread, where it "
                f"would block the loop it needs to make progress. Use "
                f"`await clock.{what}(...)` here."
            )
        asyncio.run_coroutine_threadsafe(coro, loop).result()

    def _wake_instant(self, seconds: float) -> float:
        # Negative durations are tolerated rather than rejected, per the Clock contract:
        # callers compute `deadline - now()`, which goes negative once a deadline passes.
        return self.now() + max(0.0, seconds)

    def _publish(self, at: float) -> None:
        with self._state_lock:
            self._now = at
            self._pinned = True

    def _unpin(self) -> None:
        # Follow real time again rather than freezing at the reading taken here: the engine
        # is ticking, and a single stored sample would leave the mirror stopped.
        with self._state_lock:
            self._pinned = False

    def _require_async(self, what: str) -> None:
        if not self._is_async:
            # Awaiting a sync client would block the loop on an HTTP round trip.
            raise RuntimeError(
                f"This EngineClock is bound to a synchronous client; use "
                f"clock.{what}_sync(), or construct it with CamundaAsyncClient."
            )

    @staticmethod
    def _current_owner() -> object:
        try:
            task = asyncio.current_task()
        except RuntimeError:
            task = None
        return task if task is not None else threading.get_ident()

    def _guard_reentry(self) -> None:
        # Only the caller that is *itself* mid-pin is re-entering; anyone else is ordinary
        # concurrency and belongs in the queue behind the lock. Checked before the lock, not
        # inside it: neither lock is reentrant, so a genuine re-entry would deadlock here
        # rather than reach this message.
        #
        # Compared by value, not identity: the sync owner is a thread id, and
        # `threading.get_ident()` returns an int too large for CPython's small-int cache, so
        # two calls on one thread are equal but not the same object. `is` here let same-thread
        # re-entry through to exactly the deadlock this guard exists to prevent.
        owner = self._pin_owner
        if owner is not None and owner == self._current_owner():
            raise RuntimeError(
                "EngineClock re-entered while pinning: the request it issues is itself "
                "waiting on this clock. Point the clock at a client other than the one it "
                "is injected into."
            )

    async def _pin_async(self, at: float) -> None:
        self._pin_owner = self._current_owner()
        try:
            await self._call(self._target.pin_clock(data=_pin_request(at)))
        finally:
            self._pin_owner = None
        # Only once the engine has accepted it: a failed pin must not leave the mirror
        # reporting a time the engine never adopted.
        self._publish(at)

    def _pin_sync(self, at: float) -> None:
        self._pin_owner = self._current_owner()
        try:
            self._target.pin_clock(data=_pin_request(at))
        finally:
            self._pin_owner = None
        self._publish(at)

    @staticmethod
    async def _call(result: Awaitable[None] | None) -> None:
        if inspect.isawaitable(result):
            await result


def _pin_request(at: float) -> ClockPinRequest:
    # The engine takes epoch milliseconds; this clock speaks seconds.
    return ClockPinRequest(timestamp=int(at * 1000))
