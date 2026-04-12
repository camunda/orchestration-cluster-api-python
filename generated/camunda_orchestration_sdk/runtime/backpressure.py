"""Adaptive semaphore-based global backpressure controller.

Escalates on broker backpressure signals, throttles initiating operations.
Exempt operations (e.g., job completion/failure) bypass acquire.

Two profiles:
- BALANCED (default): adaptive gating with AIMD-style recovery
- LEGACY: observe-only, record severity but never gate

Ported from the TypeScript SDK implementation.
"""

from __future__ import annotations

import asyncio
import math
import threading
import time as _time_module
from typing import Literal, Protocol, TypedDict

from .logging import SdkLogger

BackpressureSeverity = Literal["healthy", "soft", "severe"]
BackpressureProfile = Literal["BALANCED", "LEGACY"]


class BackpressureState(TypedDict):
    severity: BackpressureSeverity
    consecutive: int
    permits_max: int | None
    permits_current: int
    waiters: int
    backoff_ms: int


class _Clock(Protocol):
    def time(self) -> float: ...


# Exempt methods that should bypass gating (drain work / complete execution).
EXEMPT_METHODS: frozenset[str] = frozenset(
    {
        "complete_job",
        "fail_job",
        "throw_job_error",
        "complete_user_task",
    }
)

# BALANCED profile defaults (matching TypeScript SDK).
_INITIAL_MAX: int = 16
_FLOOR: int = 1
_SOFT_FACTOR: float = 0.70
_SEVERE_FACTOR: float = 0.50
_RECOVERY_INTERVAL_S: float = 1.0
_RECOVERY_STEP: int = 1
_SEVERE_THRESHOLD: int = 3
_DECAY_QUIET_S: float = 2.0
_MAX_WAITERS: int = 1000
_HEALTHY_RECOVERY_MULTIPLIER: float = 1.5
_UNLIMITED_AFTER_HEALTHY_S: float = 30.0

# Backoff-at-floor: rate-limit when concurrency can't drop further.
_BACKOFF_INITIAL_S: float = 0.025  # 25ms initial delay
_BACKOFF_MAX_S: float = 2.0  # ceiling
_BACKOFF_ESCALATE: float = 2.0  # double on each 429 at floor


class BackpressureQueueFull(Exception):
    """Raised when the waiter queue is at capacity."""


def is_backpressure_response(status_code: int, body: str | None = None) -> bool:
    """Return True if the HTTP response signals cluster backpressure."""
    if status_code == 429:
        return True
    if status_code == 503:
        if body and "RESOURCE_EXHAUSTED" in body:
            return True
        # Treat bare 503 as backpressure (matches TS SDK behaviour).
        if not body:
            return True
    if status_code == 500 and body and "RESOURCE_EXHAUSTED" in body:
        return True
    return False


def is_backpressure_error(exc: Exception) -> bool:
    """Check if an exception represents a backpressure signal.

    Works with any exception that has ``status_code`` (int) and ``content`` (bytes)
    attributes — in particular the SDK's ``ApiError`` family.
    """
    status_code = getattr(exc, "status_code", None)
    if status_code is None:
        return False
    content = getattr(exc, "content", None)
    body = content.decode(errors="ignore") if isinstance(content, bytes) else None
    return is_backpressure_response(status_code, body)


class BackpressureManager:
    """Thread-safe adaptive backpressure manager for the sync CamundaClient.

    Uses ``threading.Semaphore`` for permit gating and ``threading.Lock``
    for internal state.
    """

    def __init__(
        self,
        *,
        profile: BackpressureProfile = "BALANCED",
        logger: SdkLogger | None = None,
        clock: _Clock | None = None,
    ) -> None:
        self._logger = logger
        self._clock: _Clock = clock or _time_module
        self._lock = threading.Lock()
        self._observe_only = profile == "LEGACY"

        # State
        self._severity: BackpressureSeverity = "healthy"
        self._consecutive: int = 0
        self._last_event_at: float = 0.0
        self._permits_current: int = 0
        # Start unlimited — only boot to _INITIAL_MAX on first BP signal
        self._permits_max: int | None = None
        self._last_recover_check: float = 0.0
        self._healthy_since: float = 0.0

        # Waiter queue (condition-variable based)
        self._waiters: int = 0
        self._condition = threading.Condition(self._lock)

        # Backoff-at-floor: rate-limit when at concurrency floor + severe
        self._backoff_s: float = 0.0

    @property
    def severity(self) -> BackpressureSeverity:
        return self._severity

    def get_state(self) -> BackpressureState:
        with self._lock:
            return {
                "severity": self._severity,
                "consecutive": self._consecutive,
                "permits_max": self._permits_max,
                "permits_current": self._permits_current,
                "waiters": self._waiters,
                "backoff_ms": round(self._backoff_s * 1000),
            }

    def acquire(self) -> None:
        """Block until a permit is available. Raises BackpressureQueueFull
        if the waiter queue is at capacity."""
        if self._observe_only:
            return
        # Backoff-at-floor: sleep outside the lock to rate-limit at floor
        backoff = 0.0
        with self._lock:
            if self._permits_max is None:
                return  # unlimited fast path
            backoff = self._backoff_s
        if backoff > 0:
            _time_module.sleep(backoff)
        with self._lock:
            if self._permits_max is None:  # pyright: ignore[reportUnnecessaryComparison]  # value can change during sleep
                return  # went unlimited during backoff
            # Immediate acquire
            if self._permits_current < self._permits_max:
                self._permits_current += 1
                return
            # Fail-fast if waiter queue full
            if self._waiters >= _MAX_WAITERS:
                raise BackpressureQueueFull(
                    f"Backpressure waiter queue full ({_MAX_WAITERS}). "
                    "Rejecting to prevent unbounded memory growth."
                )
            # Wait
            self._waiters += 1
            try:
                while True:
                    pm: int | None = self._permits_max
                    if pm is None:  # pyright: ignore[reportUnnecessaryComparison]  # value can change during wait()
                        # Went unlimited while waiting
                        self._waiters -= 1
                        return
                    if self._permits_current < pm:
                        break
                    self._condition.wait()
                self._permits_current += 1
            finally:
                self._waiters -= 1

    def release(self) -> None:
        """Release a permit and wake one waiter if queued."""
        if self._observe_only:
            return
        with self._lock:
            if self._permits_max is None:
                return
            if self._permits_current > 0:
                self._permits_current -= 1
            self._condition.notify()

    def record_backpressure(self) -> None:
        """Record a backpressure signal from the server."""
        now = self._clock.time()
        with self._lock:
            self._last_event_at = now
            self._consecutive += 1
            self._healthy_since = 0.0

            if not self._observe_only:
                # Boot to initial cap on first BP signal (was unlimited)
                if self._permits_max is None:
                    self._permits_max = _INITIAL_MAX
                    self._permits_current = min(
                        self._permits_current, self._permits_max
                    )

            prev = self._severity
            if self._consecutive >= _SEVERE_THRESHOLD:
                self._severity = "severe"
                if not self._observe_only:
                    self._scale_permits(_SEVERE_FACTOR)
            elif self._severity == "healthy":
                self._severity = "soft"
                if not self._observe_only:
                    self._scale_permits(_SOFT_FACTOR)
            else:
                # Already soft — keep scaling with soft factor
                if not self._observe_only:
                    self._scale_permits(_SOFT_FACTOR)

            # Escalate backoff when stuck at floor + severe
            if (
                not self._observe_only
                and self._permits_max is not None
                and self._permits_max <= _FLOOR
                and self._severity == "severe"
            ):
                if self._backoff_s == 0.0:
                    self._backoff_s = _BACKOFF_INITIAL_S
                else:
                    self._backoff_s = min(
                        _BACKOFF_MAX_S,
                        self._backoff_s * _BACKOFF_ESCALATE,
                    )
                self._log_debug(
                    "bp.backoff.escalate",
                    {"delay_ms": round(self._backoff_s * 1000)},
                )

            if self._severity != prev:
                self._log_severity(prev, self._severity)

    def record_healthy_hint(self) -> None:
        """Record a successful (non-backpressure) completion. Triggers passive recovery."""
        now = self._clock.time()
        with self._lock:
            # Reset backoff immediately on success — server has capacity
            if self._backoff_s > 0:
                self._backoff_s = 0.0
            self._maybe_recover(now)

    def _scale_permits(self, factor: float) -> None:
        """Reduce permits by factor (must hold lock)."""
        if self._permits_max is None:
            return
        next_max = max(_FLOOR, math.ceil(self._permits_max * factor))
        if next_max < self._permits_max:
            self._permits_max = next_max
            self._log_debug("bp.permits.scale", {"max": self._permits_max})

    def _maybe_recover(self, now: float) -> None:
        """Passive recovery check (must hold lock)."""
        if self._permits_max is None or self._observe_only:
            return
        if now - self._last_recover_check < _RECOVERY_INTERVAL_S:
            return
        self._last_recover_check = now

        # Decay severity if quiet (stepwise: severe→soft→healthy)
        if now - self._last_event_at > _DECAY_QUIET_S:
            prev = self._severity
            if self._severity == "severe":
                self._severity = "soft"
            elif self._severity == "soft":
                self._severity = "healthy"
                self._healthy_since = now
            if self._severity == "healthy":
                self._consecutive = 0
            if prev != self._severity:
                # Clear backoff when severity improves
                if self._backoff_s > 0:
                    self._backoff_s = 0.0
                    self._log_debug("bp.backoff.clear", {"reason": "severity-decay"})
                self._log_severity(prev, self._severity)

        # Recovery phases
        bootstrap_cap = _INITIAL_MAX
        if self._severity != "healthy":
            # Phase 1: additive recovery while not yet healthy
            if self._permits_max < bootstrap_cap:
                self._permits_max = min(
                    bootstrap_cap, self._permits_max + _RECOVERY_STEP
                )
                # Clear backoff when leaving floor
                if self._permits_max > _FLOOR and self._backoff_s > 0:
                    self._backoff_s = 0.0
                    self._log_debug("bp.backoff.clear", {"reason": "left-floor"})
                self._log_debug(
                    "bp.permits.recover",
                    {"max": self._permits_max, "phase": "additive"},
                )
                self._condition.notify()
            return

        # Phase 3: sustained healthy → return to unlimited
        if (
            self._healthy_since > 0
            and now - self._healthy_since >= _UNLIMITED_AFTER_HEALTHY_S
        ):
            self._permits_max = None
            self._permits_current = 0
            self._backoff_s = 0.0
            self._condition.notify_all()
            self._log_debug(
                "bp.permits.unlimited",
                {"reason": "sustained-healthy"},
            )
            return

        # Phase 2: multiplicative growth while healthy (no ceiling)
        next_max = math.ceil(self._permits_max * _HEALTHY_RECOVERY_MULTIPLIER)
        if next_max > self._permits_max:
            self._permits_max = next_max
            self._log_debug(
                "bp.permits.recover",
                {"max": self._permits_max, "phase": "multiplicative"},
            )
            self._condition.notify()

    def _log_severity(self, prev: str, curr: str) -> None:
        if self._logger is None:
            return
        entering_unhealthy = prev == "healthy" and curr != "healthy"
        recovering = prev != "healthy" and curr == "healthy"
        if entering_unhealthy or recovering:
            self._logger.info(f"bp.state.change from={prev} to={curr}")
        else:
            self._logger.debug(f"bp.state.change from={prev} to={curr}")

    def _log_debug(self, event: str, data: dict[str, object]) -> None:
        if self._logger is None:
            return
        self._logger.debug(f"{event} {data}")


class AsyncBackpressureManager:
    """Asyncio-based adaptive backpressure manager for the async CamundaAsyncClient.

    Uses ``asyncio.Semaphore``-style gating with ``asyncio.Condition`` and
    ``asyncio.Lock`` for internal state.
    """

    def __init__(
        self,
        *,
        profile: BackpressureProfile = "BALANCED",
        logger: SdkLogger | None = None,
        clock: _Clock | None = None,
    ) -> None:
        self._logger = logger
        self._clock: _Clock = clock or _time_module
        self._lock = asyncio.Lock()
        self._observe_only = profile == "LEGACY"

        # State
        self._severity: BackpressureSeverity = "healthy"
        self._consecutive: int = 0
        self._last_event_at: float = 0.0
        self._permits_current: int = 0
        # Start unlimited — only boot to _INITIAL_MAX on first BP signal
        self._permits_max: int | None = None
        self._last_recover_check: float = 0.0
        self._healthy_since: float = 0.0

        # Waiter queue (condition-variable based)
        self._waiters: int = 0
        self._condition = asyncio.Condition(self._lock)

        # Backoff-at-floor: rate-limit when at concurrency floor + severe
        self._backoff_s: float = 0.0

    @property
    def severity(self) -> BackpressureSeverity:
        return self._severity

    def get_state(self) -> BackpressureState:
        # Lock-free read of approximate state (acceptable for observability).
        return {
            "severity": self._severity,
            "consecutive": self._consecutive,
            "permits_max": self._permits_max,
            "permits_current": self._permits_current,
            "waiters": self._waiters,
            "backoff_ms": round(self._backoff_s * 1000),
        }

    async def acquire(self) -> None:
        """Await until a permit is available."""
        if self._observe_only:
            return
        # Backoff-at-floor: sleep outside the lock to rate-limit at floor
        backoff = 0.0
        async with self._lock:
            if self._permits_max is None:
                return
            backoff = self._backoff_s
        if backoff > 0:
            await asyncio.sleep(backoff)
        async with self._lock:
            if self._permits_max is None:  # pyright: ignore[reportUnnecessaryComparison]  # value can change during sleep
                return  # went unlimited during backoff
            if self._permits_current < self._permits_max:
                self._permits_current += 1
                return
            if self._waiters >= _MAX_WAITERS:
                raise BackpressureQueueFull(
                    f"Backpressure waiter queue full ({_MAX_WAITERS}). "
                    "Rejecting to prevent unbounded memory growth."
                )

        # Must wait outside the lock so others can release.
        async with self._condition:
            self._waiters += 1
            try:
                while True:
                    pm: int | None = self._permits_max
                    if pm is None:  # pyright: ignore[reportUnnecessaryComparison]  # value can change during wait()
                        return
                    if self._permits_current < pm:
                        break
                    await self._condition.wait()
                self._permits_current += 1
            finally:
                self._waiters -= 1

    async def release(self) -> None:
        if self._observe_only:
            return
        async with self._condition:
            if self._permits_max is None:
                return
            if self._permits_current > 0:
                self._permits_current -= 1
            self._condition.notify()

    async def record_backpressure(self) -> None:
        now = self._clock.time()
        async with self._lock:
            self._last_event_at = now
            self._consecutive += 1
            self._healthy_since = 0.0

            if not self._observe_only:
                # Boot to initial cap on first BP signal (was unlimited)
                if self._permits_max is None:
                    self._permits_max = _INITIAL_MAX
                    self._permits_current = min(
                        self._permits_current, self._permits_max
                    )

            prev = self._severity
            if self._consecutive >= _SEVERE_THRESHOLD:
                self._severity = "severe"
                if not self._observe_only:
                    self._scale_permits(_SEVERE_FACTOR)
            elif self._severity == "healthy":
                self._severity = "soft"
                if not self._observe_only:
                    self._scale_permits(_SOFT_FACTOR)
            else:
                if not self._observe_only:
                    self._scale_permits(_SOFT_FACTOR)

            # Escalate backoff when stuck at floor + severe
            if (
                not self._observe_only
                and self._permits_max is not None
                and self._permits_max <= _FLOOR
                and self._severity == "severe"
            ):
                if self._backoff_s == 0.0:
                    self._backoff_s = _BACKOFF_INITIAL_S
                else:
                    self._backoff_s = min(
                        _BACKOFF_MAX_S,
                        self._backoff_s * _BACKOFF_ESCALATE,
                    )
                self._log_debug(
                    "bp.backoff.escalate",
                    {"delay_ms": round(self._backoff_s * 1000)},
                )

            if self._severity != prev:
                self._log_severity(prev, self._severity)

    async def record_healthy_hint(self) -> None:
        now = self._clock.time()
        async with self._lock:
            # Reset backoff immediately on success — server has capacity
            if self._backoff_s > 0:
                self._backoff_s = 0.0
            self._maybe_recover(now)

    def _scale_permits(self, factor: float) -> None:
        """Reduce permits by factor (must hold lock)."""
        if self._permits_max is None:
            return
        next_max = max(_FLOOR, math.ceil(self._permits_max * factor))
        if next_max < self._permits_max:
            self._permits_max = next_max
            self._log_debug("bp.permits.scale", {"max": self._permits_max})

    def _maybe_recover(self, now: float) -> None:
        """Passive recovery check (must hold lock)."""
        if self._permits_max is None or self._observe_only:
            return
        if now - self._last_recover_check < _RECOVERY_INTERVAL_S:
            return
        self._last_recover_check = now

        # Decay severity if quiet (stepwise: severe→soft→healthy)
        if now - self._last_event_at > _DECAY_QUIET_S:
            prev = self._severity
            if self._severity == "severe":
                self._severity = "soft"
            elif self._severity == "soft":
                self._severity = "healthy"
                self._healthy_since = now
            if self._severity == "healthy":
                self._consecutive = 0
            if prev != self._severity:
                # Clear backoff when severity improves
                if self._backoff_s > 0:
                    self._backoff_s = 0.0
                    self._log_debug("bp.backoff.clear", {"reason": "severity-decay"})
                self._log_severity(prev, self._severity)

        # Recovery phases
        bootstrap_cap = _INITIAL_MAX
        if self._severity != "healthy":
            # Phase 1: additive recovery while not yet healthy
            if self._permits_max < bootstrap_cap:
                self._permits_max = min(
                    bootstrap_cap, self._permits_max + _RECOVERY_STEP
                )
                # Clear backoff when leaving floor
                if self._permits_max > _FLOOR and self._backoff_s > 0:
                    self._backoff_s = 0.0
                    self._log_debug("bp.backoff.clear", {"reason": "left-floor"})
                self._log_debug(
                    "bp.permits.recover",
                    {"max": self._permits_max, "phase": "additive"},
                )
            return

        # Phase 3: sustained healthy → return to unlimited
        if (
            self._healthy_since > 0
            and now - self._healthy_since >= _UNLIMITED_AFTER_HEALTHY_S
        ):
            self._permits_max = None
            self._permits_current = 0
            self._backoff_s = 0.0
            self._log_debug(
                "bp.permits.unlimited",
                {"reason": "sustained-healthy"},
            )
            return

        # Phase 2: multiplicative growth while healthy (no ceiling)
        next_max = math.ceil(self._permits_max * _HEALTHY_RECOVERY_MULTIPLIER)
        if next_max > self._permits_max:
            self._permits_max = next_max
            self._log_debug(
                "bp.permits.recover",
                {"max": self._permits_max, "phase": "multiplicative"},
            )

    def _log_severity(self, prev: str, curr: str) -> None:
        if self._logger is None:
            return
        entering_unhealthy = prev == "healthy" and curr != "healthy"
        recovering = prev != "healthy" and curr == "healthy"
        if entering_unhealthy or recovering:
            self._logger.info(f"bp.state.change from={prev} to={curr}")
        else:
            self._logger.debug(f"bp.state.change from={prev} to={curr}")

    def _log_debug(self, event: str, data: dict[str, object]) -> None:
        if self._logger is None:
            return
        self._logger.debug(f"{event} {data}")
