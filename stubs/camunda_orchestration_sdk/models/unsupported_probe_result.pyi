from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define

T = TypeVar("T", bound="UnsupportedProbeResult")

@_attrs_define
class UnsupportedProbeResult:
    outcome: str
    worker: str
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
