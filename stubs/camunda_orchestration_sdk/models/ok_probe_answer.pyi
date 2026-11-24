from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.probe_ok_result_data import ProbeOkResultData

T = TypeVar("T", bound="OKProbeAnswer")

@_attrs_define
class OKProbeAnswer:
    outcome: str
    data: ProbeOkResultData
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
