"""The incident, inverted.

The failure that started all of this: a worker polling for a process that only completes
after the engine's clock moves. Pin the engine and the worker keeps waiting on the real
clock; drive the worker's clock and the engine never reaches the timer. It burns a real
minute either way.

With `EngineClock` there is one clock. The worker's poll interval and the engine's time are
the same quantity, so a minute of engine time passes in real milliseconds -- and, critically,
the engine really is moved: the pins below are the requests a live engine would have received.

This is the acceptance criterion for camunda/orchestration-cluster-api-js#450 in Python. It
is deliberately written against the SDK's real poll loops rather than a stub, because the
defect it guards was precisely that the seam looked correct while the loops ignored it.
"""

from __future__ import annotations

import time as real_time

import pytest

from camunda_orchestration_sdk.runtime.clock import EngineClock
from camunda_orchestration_sdk.runtime.eventual import (
    ConsistencyOptions,
    EventualConsistencyTimeoutError,
    eventual_poll_async,
)

#: Engine time the poller spans. A real minute of polling would be unmistakable in the run.
ENGINE_MINUTE_MS = 60_000

#: Real seconds the whole thing may take. A safety net, not a timing assertion.
REAL_BUDGET_S = 5.0


class RecordingEngine:
    """`PUT /clock` is write-only, so the only way to see engine time move is to record the
    pins the SDK sends."""

    def __init__(self) -> None:
        self.pins: list[int] = []

    async def pin_clock(self, *, data, **kwargs) -> None:
        self.pins.append(data.timestamp)

    async def reset_clock(self, **kwargs) -> None: ...


@pytest.mark.asyncio
async def test_a_minute_of_engine_time_passes_in_real_milliseconds() -> None:
    engine = RecordingEngine()
    clock = EngineClock(engine, start=1_700_000_000.0)
    attempts = 0

    async def never_ready() -> None:
        nonlocal attempts
        attempts += 1
        return None

    started = real_time.monotonic()
    with pytest.raises(EventualConsistencyTimeoutError) as caught:
        await eventual_poll_async(
            "getProcessInstance",
            True,
            never_ready,
            ConsistencyOptions(wait_up_to_ms=ENGINE_MINUTE_MS),
            None,
            clock,
        )
    elapsed = real_time.monotonic() - started

    assert attempts > 1, "the poller never retried, so nothing was being waited on"

    assert caught.value.elapsed_ms >= ENGINE_MINUTE_MS, (
        "the poller gave up before a minute of engine time had passed"
    )
    assert elapsed < REAL_BUDGET_S, (
        f"a minute of engine time took {elapsed:.1f}s of real time -- the poll loop is not "
        "resolving through the engine clock"
    )

    # The half that a virtual clock alone cannot give: the engine was really moved.
    assert engine.pins, "engine time never advanced; only the client's view of it did"
    assert engine.pins == sorted(engine.pins), (
        f"engine time went backwards across the poll loop: {engine.pins}"
    )
    assert engine.pins[-1] - engine.pins[0] >= ENGINE_MINUTE_MS - 1_000, (
        f"the engine advanced {engine.pins[-1] - engine.pins[0]}ms, not the ~{ENGINE_MINUTE_MS}ms "
        "the poller waited"
    )


@pytest.mark.asyncio
async def test_the_client_and_the_engine_agree_on_the_time() -> None:
    """The two clocks staying in step is the whole property; drift is the bug."""
    engine = RecordingEngine()
    clock = EngineClock(engine, start=1_700_000_000.0)

    for _ in range(10):
        await clock.sleep(6.0)

    assert clock.now() == pytest.approx(1_700_000_060.0)
    assert engine.pins[-1] == 1_700_000_060_000, (
        "the engine's last pinned time must match what the client thinks the time is"
    )
