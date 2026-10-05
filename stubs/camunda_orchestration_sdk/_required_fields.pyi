from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

V = TypeVar("V")

class RequiredFields(dict[str, V]):
    def __init__(self, src: Mapping[str, V], model: str) -> None: ...
    def pop_required(self, key: str) -> V: ...
