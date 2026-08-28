"""The clock all SDK runtime cadence resolves through.

Worker poll loops, eventual-consistency polling, retry backoff, backpressure decay and
auth refresh all resolve time here. Pinning this pins the client's own timing, which is
what makes those loops testable without waiting for real time, and what lets a later
engine-bound implementation advance client cadence and engine time together.

See the cross-SDK contract in camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import asyncio
import time as _time
from collections.abc import Callable
from typing import Protocol, runtime_checkable

__all__ = ["Clock", "LiveClock", "live_clock"]


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
    """

    def __init__(self, source: Callable[[], float] | None = None) -> None:
        # Called through rather than captured, so a test that patches the time module still
        # drives an already-constructed clock.
        self._source = source if source is not None else (lambda: _time.time())
        self._last_source = self._source()
        self._offset = 0.0

    def now(self) -> float:
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
