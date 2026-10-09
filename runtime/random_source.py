"""The randomness all SDK runtime jitter resolves through.

The randomness counterpart of :class:`~camunda_orchestration_sdk.runtime.clock.Clock`:
pinning the clock makes cadence virtual, injecting a :class:`SeededRandom` as well makes it
reproducible. See the cross-SDK contract in camunda/sdk-infra#50.
"""

from __future__ import annotations

import os
import random as _random  # noqa: TID251 — the live source is the one place the platform generator is read
import re
import threading
from collections.abc import Mapping
from typing import Protocol, runtime_checkable

__all__ = [
    "SEED_ENV_VAR",
    "LiveRandom",
    "RandomSource",
    "SeededRandom",
    "live_random",
]

#: Environment variable :meth:`SeededRandom.from_env` reads to replay a seed.
SEED_ENV_VAR = "CAMUNDA_TEST_SEED"

_MASK_64 = (1 << 64) - 1
_GAMMA = 0x9E3779B97F4A7C15
_UNIT = 2.0**-53


@runtime_checkable
class RandomSource(Protocol):
    """Randomness as the SDK runtime sees it. Implementations must be thread-safe."""

    def next(self) -> float:
        """A uniformly distributed value in ``[0, 1)``."""
        ...


class LiveRandom:
    """The platform generator. Production jitter stays random so a fleet of workers does not
    start or retry in lockstep."""

    def next(self) -> float:
        return _random.random()  # noqa: S311 — jitter, not security-sensitive


#: The randomness source used when none is injected.
live_random: RandomSource = LiveRandom()


class SeededRandom:
    """A deterministic source for tests: the same seed yields the same draws on every run, and
    in every Camunda SDK.

    SplitMix64, taking the top 53 bits of each output. Specified by the cross-SDK contract
    rather than borrowed from :mod:`random`, so a seed reproduces the same jitter in any SDK.
    Reproducibility holds for draws made in a fixed order.
    """

    def __init__(self, seed: int) -> None:
        # bool is an int subclass, so True would otherwise pass as seed 1.
        if type(seed) is not int or not 0 <= seed <= _MASK_64:
            raise ValueError(f"seed must be an unsigned 64-bit integer, got {seed!r}")
        self._seed = seed
        self._state = seed
        self._lock = threading.Lock()

    @property
    def seed(self) -> int:
        """Report this on failure to make the run replayable."""
        return self._seed

    def next(self) -> float:
        with self._lock:
            self._state = (self._state + _GAMMA) & _MASK_64
            z = self._state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _MASK_64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _MASK_64
        z ^= z >> 31
        return (z >> 11) * _UNIT

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> SeededRandom:
        """Seed from ``CAMUNDA_TEST_SEED`` when it is set, otherwise from a fresh random seed.

        Only an unset variable means "absent": any other value that is not an unsigned 64-bit
        decimal integer raises rather than silently replacing the seed being replayed.
        """
        raw = (os.environ if env is None else env).get(SEED_ENV_VAR)
        if raw is None:
            return cls(int(live_random.next() * 2**53))
        if re.fullmatch(r"[0-9]+", raw) is None or int(raw) > _MASK_64:
            raise ValueError(f"{SEED_ENV_VAR}={raw!r} is not an unsigned 64-bit decimal integer.")
        return cls(int(raw))

    def __repr__(self) -> str:
        return f"SeededRandom(seed={self._seed}; replay with {SEED_ENV_VAR}={self._seed})"
