"""The `Clock` contract, as an executable suite.

Every `Clock` implementation is checked against the same clauses. A lint rule can ban
ambient time, but it cannot tell whether an implementation honours its own protocol — in
the JS slice that gap let three broken clocks reach review, so the suite exists here from
the start rather than being retrofitted.

To cover a new implementation, add it to ``SUBJECT_FACTORIES`` in test_clock_contract.py.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from camunda_orchestration_sdk.runtime.clock import Clock


@dataclass
class ClockSubject:
    """A clock under test, plus the means to move it forward.

    The live clock advances by real waiting; a virtual clock advances on command. Every
    other clause is shared.
    """

    name: str
    clock: Clock
    advance: Callable[[float], Awaitable[None]]


#: Real seconds the clauses that cannot be virtualised wait on. Small, because they are
#: paid on every implementation.
REAL_S = 0.05


async def assert_now_reports_epoch_seconds(subject: ClockSubject) -> None:
    now = subject.clock.now()
    assert isinstance(now, float), f"{subject.name}: now() must return a float"
    assert now >= 0.0, f"{subject.name}: now() must be non-negative, got {now}"


async def assert_now_never_goes_backwards(subject: ClockSubject) -> None:
    readings = [subject.clock.now()]
    for _ in range(5):
        await subject.advance(REAL_S)
        readings.append(subject.clock.now())

    assert readings == sorted(readings), f"{subject.name}: now() went backwards: {readings}"


async def assert_sleep_yields(subject: ClockSubject) -> None:
    """The clause hand-rolled clocks break most often.

    The worker schedules its next poll by awaiting sleep, so an implementation that
    returns without yielding turns the loop into a spin.
    """
    settled = False

    async def waiter() -> None:
        nonlocal settled
        await subject.clock.sleep(REAL_S)
        settled = True

    task = asyncio.ensure_future(waiter())
    # Give the event loop a step. Anything that completed without yielding shows up here.
    await asyncio.sleep(0)
    assert not settled, f"{subject.name}: sleep() completed without yielding"

    await subject.advance(REAL_S)
    await task
    assert settled, f"{subject.name}: sleep() never completed"


async def assert_sleep_waits_for_the_clock(subject: ClockSubject) -> None:
    before = subject.clock.now()
    await subject.clock.sleep(REAL_S)
    after = subject.clock.now()

    assert after >= before, f"{subject.name}: time moved backwards across a sleep"


async def assert_sleep_sync_waits(subject: ClockSubject) -> None:
    before = subject.clock.now()
    subject.clock.sleep_sync(REAL_S)
    after = subject.clock.now()

    assert after >= before, f"{subject.name}: sleep_sync moved time backwards"


async def assert_negative_sleeps_are_tolerated(subject: ClockSubject) -> None:
    """A negative duration is already elapsed, so it returns rather than raising.

    Callers compute ``deadline - now()``, which goes negative the moment a deadline
    passes; raising there would turn an ordinary timeout into a crash.
    """
    await subject.clock.sleep(-1.0)
    subject.clock.sleep_sync(-1.0)


#: Every clause, in the order a reader wants them.
CONTRACT: tuple[Callable[[ClockSubject], Awaitable[None]], ...] = (
    assert_now_reports_epoch_seconds,
    assert_now_never_goes_backwards,
    assert_sleep_yields,
    assert_sleep_waits_for_the_clock,
    assert_sleep_sync_waits,
    assert_negative_sleeps_are_tolerated,
)
