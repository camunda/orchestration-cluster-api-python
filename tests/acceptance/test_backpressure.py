"""Acceptance tests for the adaptive backpressure manager."""

from __future__ import annotations

import pytest

from camunda_orchestration_sdk.runtime.backpressure import (
    AsyncBackpressureManager,
    BackpressureManager,
    BackpressureQueueFull,
    EXEMPT_METHODS,
    is_backpressure_error,
    is_backpressure_response,
)

# Re-declare constants used by tests (mirrors runtime defaults).
_DECAY_QUIET_S: float = 2.0
_INITIAL_MAX: int = 16
_MAX_WAITERS: int = 1000
_RECOVERY_INTERVAL_S: float = 1.0
_SEVERE_THRESHOLD: int = 3
_SOFT_FACTOR: float = 0.70
_UNLIMITED_AFTER_HEALTHY_S: float = 30.0


# ---------------------------------------------------------------------------
# Fake clock for deterministic time control
# ---------------------------------------------------------------------------


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def time(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


# ---------------------------------------------------------------------------
# is_backpressure_response
# ---------------------------------------------------------------------------


class TestIsBackpressureResponse:
    def test_429_is_backpressure(self):
        assert is_backpressure_response(429) is True

    def test_503_with_resource_exhausted(self):
        assert is_backpressure_response(503, "RESOURCE_EXHAUSTED") is True

    def test_503_bare(self):
        assert is_backpressure_response(503) is True

    def test_500_with_resource_exhausted(self):
        assert is_backpressure_response(500, "RESOURCE_EXHAUSTED") is True

    def test_500_without_resource_exhausted(self):
        assert is_backpressure_response(500, "Internal error") is False

    def test_200_not_backpressure(self):
        assert is_backpressure_response(200) is False


# ---------------------------------------------------------------------------
# is_backpressure_error
# ---------------------------------------------------------------------------


class TestIsBackpressureError:
    def test_with_status_code_and_content(self):
        class FakeError(Exception):
            status_code = 429
            content = b"Too Many Requests"

        assert is_backpressure_error(FakeError()) is True

    def test_with_non_backpressure_error(self):
        class FakeError(Exception):
            status_code = 404
            content = b"Not Found"

        assert is_backpressure_error(FakeError()) is False

    def test_with_plain_exception(self):
        assert is_backpressure_error(Exception("boom")) is False


# ---------------------------------------------------------------------------
# EXEMPT_METHODS
# ---------------------------------------------------------------------------


def test_exempt_methods_is_frozen():
    assert isinstance(EXEMPT_METHODS, frozenset)
    assert "complete_job" in EXEMPT_METHODS
    assert "fail_job" in EXEMPT_METHODS
    assert "throw_job_error" in EXEMPT_METHODS
    assert "complete_user_task" in EXEMPT_METHODS


# ---------------------------------------------------------------------------
# BackpressureManager (sync, BALANCED)
# ---------------------------------------------------------------------------


class TestBackpressureManagerBalanced:
    def _make(
        self, clock: FakeClock | None = None
    ) -> tuple[BackpressureManager, FakeClock]:
        clk = clock or FakeClock()
        return BackpressureManager(profile="BALANCED", clock=clk), clk

    def test_starts_healthy_unlimited(self):
        bp, _ = self._make()
        state = bp.get_state()
        assert state["severity"] == "healthy"
        assert state["permits_max"] is None  # unlimited until first BP

    def test_acquire_when_unlimited(self):
        bp, _ = self._make()
        bp.acquire()  # should not raise (unlimited)
        bp.release()

    def test_first_signal_boots_to_soft(self):
        bp, _ = self._make()
        bp.record_backpressure()
        state = bp.get_state()
        assert state["severity"] == "soft"
        assert state["permits_max"] is not None
        # Boots to _INITIAL_MAX then scales by soft factor
        import math

        expected = max(1, math.ceil(_INITIAL_MAX * _SOFT_FACTOR))
        assert state["permits_max"] == expected

    def test_first_signal_sets_initial_max(self):
        bp, _ = self._make()
        bp.record_backpressure()
        state = bp.get_state()
        import math

        expected = max(1, math.ceil(_INITIAL_MAX * _SOFT_FACTOR))
        assert state["permits_max"] == expected

    def test_severe_after_threshold(self):
        bp, _ = self._make()
        for _ in range(_SEVERE_THRESHOLD):
            bp.record_backpressure()
        assert bp.severity == "severe"

    def test_permits_decrease_on_severe(self):
        bp, _ = self._make()
        # First signal: boots & scales to soft
        bp.record_backpressure()
        soft_max = bp.get_state()["permits_max"]
        # Continue to severe
        for _ in range(_SEVERE_THRESHOLD - 1):
            bp.record_backpressure()
        severe_max = bp.get_state()["permits_max"]
        assert severe_max is not None
        assert soft_max is not None
        assert severe_max < soft_max  # type: ignore[operator]

    def test_recovery_additive_then_multiplicative(self):
        bp, clk = self._make()
        bp.record_backpressure()
        max_after_signal = bp.get_state()["permits_max"]
        assert max_after_signal is not None

        # Advance past decay quiet + recovery interval to trigger recovery
        clk.advance(_DECAY_QUIET_S + _RECOVERY_INTERVAL_S + 0.1)
        bp.record_healthy_hint()
        state = bp.get_state()
        # Should have recovered (severity decayed to healthy, permits increased)
        assert state["severity"] == "healthy"
        assert state["permits_max"] is not None
        assert state["permits_max"] > max_after_signal  # type: ignore[operator]

    def test_sustained_healthy_returns_unlimited(self):
        bp, clk = self._make()
        bp.record_backpressure()

        # Recover severity to healthy first
        clk.advance(_DECAY_QUIET_S + _RECOVERY_INTERVAL_S + 0.1)
        bp.record_healthy_hint()
        assert bp.severity == "healthy"

        # Advance past the sustained-healthy threshold
        clk.advance(_UNLIMITED_AFTER_HEALTHY_S + _RECOVERY_INTERVAL_S + 0.1)
        bp.record_healthy_hint()

        state = bp.get_state()
        assert state["permits_max"] is None  # returned to unlimited

    def test_acquire_blocks_when_at_capacity(self):
        import threading

        bp, _ = self._make()
        bp.record_backpressure()
        state = bp.get_state()
        cap = state["permits_max"]
        assert cap is not None

        # Fill up permits
        for _ in range(int(cap)):  # type: ignore[arg-type]
            bp.acquire()

        # Next acquire should block — run in a thread with timeout
        acquired = threading.Event()

        def try_acquire():
            bp.acquire()
            acquired.set()

        t = threading.Thread(target=try_acquire, daemon=True)
        t.start()
        assert not acquired.wait(timeout=0.1)

        # Release one permit → should unblock
        bp.release()
        assert acquired.wait(timeout=1.0)


# ---------------------------------------------------------------------------
# BackpressureManager (sync, LEGACY)
# ---------------------------------------------------------------------------


class TestBackpressureManagerLegacy:
    def test_legacy_never_gates(self):
        bp = BackpressureManager(profile="LEGACY")
        bp.record_backpressure()
        bp.record_backpressure()
        bp.record_backpressure()
        state = bp.get_state()
        # Severity tracks signals but permits stay unlimited
        assert state["severity"] == "severe"
        assert state["permits_max"] is None

    def test_legacy_acquire_release_noop(self):
        bp = BackpressureManager(profile="LEGACY")
        bp.record_backpressure()
        bp.acquire()  # should not block
        bp.release()  # should not raise


# ---------------------------------------------------------------------------
# BackpressureManager — queue full
# ---------------------------------------------------------------------------


class TestBackpressureQueueFull:
    def test_raise_when_waiters_at_capacity(self):
        """Verify acquire() raises BackpressureQueueFull when waiter queue is saturated.

        We directly set _waiters to the max to avoid spawning 1000+ threads in tests.
        """
        clk = FakeClock()
        bp = BackpressureManager(profile="BALANCED", clock=clk)
        bp.record_backpressure()
        cap = bp.get_state()["permits_max"]
        assert cap is not None

        # Fill permits so the next acquire must wait
        for _ in range(int(cap)):  # type: ignore[arg-type]
            bp.acquire()

        # Simulate saturated waiter queue
        bp._waiters = _MAX_WAITERS  # pyright: ignore[reportPrivateUsage]

        with pytest.raises(BackpressureQueueFull):
            bp.acquire()

        # Cleanup
        bp._waiters = 0  # pyright: ignore[reportPrivateUsage]
        for _ in range(int(cap)):  # type: ignore[arg-type]
            bp.release()


# ---------------------------------------------------------------------------
# AsyncBackpressureManager
# ---------------------------------------------------------------------------


class TestAsyncBackpressureManager:
    @pytest.mark.asyncio
    async def test_starts_healthy_unlimited(self):
        bp = AsyncBackpressureManager(profile="BALANCED")
        state = bp.get_state()
        assert state["severity"] == "healthy"
        assert state["permits_max"] is None  # unlimited until first BP

    @pytest.mark.asyncio
    async def test_signal_boots_permits(self):
        clk = FakeClock()
        bp = AsyncBackpressureManager(profile="BALANCED", clock=clk)
        await bp.record_backpressure()
        state = bp.get_state()
        assert state["severity"] == "soft"
        assert state["permits_max"] is not None

    @pytest.mark.asyncio
    async def test_legacy_observe_only(self):
        clk = FakeClock()
        bp = AsyncBackpressureManager(profile="LEGACY", clock=clk)
        await bp.record_backpressure()
        await bp.record_backpressure()
        await bp.record_backpressure()
        state = bp.get_state()
        assert state["severity"] == "severe"
        assert state["permits_max"] is None

    @pytest.mark.asyncio
    async def test_acquire_release_cycle(self):
        clk = FakeClock()
        bp = AsyncBackpressureManager(profile="BALANCED", clock=clk)
        await bp.record_backpressure()
        cap = bp.get_state()["permits_max"]
        assert cap is not None

        # Fill permits
        for _ in range(int(cap)):  # type: ignore[arg-type]
            await bp.acquire()

        # Release one and re-acquire
        await bp.release()
        await bp.acquire()  # should not hang


# ---------------------------------------------------------------------------
# Configuration integration
# ---------------------------------------------------------------------------


class TestBackpressureConfiguration:
    def test_default_profile_is_balanced(self):
        from camunda_orchestration_sdk.runtime.configuration_resolver import (
            CamundaSdkConfiguration,
        )

        config = CamundaSdkConfiguration()
        assert config.CAMUNDA_SDK_BACKPRESSURE_PROFILE == "BALANCED"

    def test_legacy_profile_accepted(self):
        from camunda_orchestration_sdk.runtime.configuration_resolver import (
            CamundaSdkConfiguration,
        )

        config = CamundaSdkConfiguration(CAMUNDA_SDK_BACKPRESSURE_PROFILE="LEGACY")
        assert config.CAMUNDA_SDK_BACKPRESSURE_PROFILE == "LEGACY"

    def test_invalid_profile_rejected(self):
        from pydantic import ValidationError
        from camunda_orchestration_sdk.runtime.configuration_resolver import (
            CamundaSdkConfiguration,
        )

        with pytest.raises(ValidationError):
            CamundaSdkConfiguration(CAMUNDA_SDK_BACKPRESSURE_PROFILE="INVALID")  # type: ignore[arg-type]

    def test_env_var_sets_profile(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("CAMUNDA_SDK_BACKPRESSURE_PROFILE", "LEGACY")
        from camunda_orchestration_sdk.runtime.configuration_resolver import (
            ConfigurationResolver,
            read_environment,
        )

        resolved = ConfigurationResolver(
            environment=read_environment(),
        ).resolve()
        assert resolved.effective.CAMUNDA_SDK_BACKPRESSURE_PROFILE == "LEGACY"
