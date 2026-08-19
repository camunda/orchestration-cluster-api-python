from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.restore_request import RestoreRequest

T = TypeVar("T", bound="ClusterRestoreRequestOverrides")

@_attrs_define
class ClusterRestoreRequestOverrides:
    additional_properties: dict[str, RestoreRequest] = _attrs_field(
        init=False, factory=dict
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> RestoreRequest: ...
    def __setitem__(self, key: str, value: RestoreRequest) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
