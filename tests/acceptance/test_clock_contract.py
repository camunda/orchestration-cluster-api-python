"""Runs the `Clock` contract against every implementation, plus LiveClock's own behaviour."""

from __future__ import annotations

import asyncio

import pytest

from camunda_orchestration_sdk.runtime.clock import Clock, LiveClock, live_clock
from camunda_orchestration_sdk.runtime.configuration_resolver import CamundaSdkConfigPartial
from clock_contract import CONTRACT, ClockSubject


def _live_subject() -> ClockSubject:
    return ClockSubject(
        name="LiveClock",
        clock=LiveClock(),
        advance=asyncio.sleep,
    )


#: Add an implementation here and it inherits the whole contract.
SUBJECT_FACTORIES = {
    "LiveClock": _live_subject,
}


@pytest.mark.parametrize("factory_name", sorted(SUBJECT_FACTORIES))
@pytest.mark.parametrize("clause", CONTRACT, ids=lambda c: c.__name__)
@pytest.mark.asyncio
async def test_clock_contract(factory_name: str, clause) -> None:
    await clause(SUBJECT_FACTORIES[factory_name]())


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
