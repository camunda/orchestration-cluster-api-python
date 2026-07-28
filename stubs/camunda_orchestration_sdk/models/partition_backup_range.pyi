from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.partition_backup_range_end import PartitionBackupRangeEnd
from ..models.partition_backup_range_start import PartitionBackupRangeStart

T = TypeVar("T", bound="PartitionBackupRange")

@_attrs_define
class PartitionBackupRange:
    partition_id: int
    start: None | PartitionBackupRangeStart
    end: None | PartitionBackupRangeEnd
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
