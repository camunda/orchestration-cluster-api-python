from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

__all__ = [
    "SEED_ENV_VAR",
    "LiveRandom",
    "RandomSource",
    "SeededRandom",
    "live_random",
]
SEED_ENV_VAR = "CAMUNDA_TEST_SEED"
_MASK_64 = (1 << 64) - 1
_GAMMA = 0x9E3779B97F4A7C15
_UNIT = 2.0**-53

@runtime_checkable
class RandomSource(Protocol):
    def next(self) -> float: ...

class LiveRandom:
    def next(self) -> float: ...

live_random: RandomSource = LiveRandom()

class SeededRandom:
    def __init__(self, seed: int) -> None: ...
    @property
    def seed(self) -> int: ...
    def next(self) -> float: ...
    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> SeededRandom: ...
    def __repr__(self) -> str: ...
