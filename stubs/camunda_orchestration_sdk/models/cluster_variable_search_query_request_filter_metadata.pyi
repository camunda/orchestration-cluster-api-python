from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_metadata_value_filter import AdvancedMetadataValueFilter

T = TypeVar("T", bound="ClusterVariableSearchQueryRequestFilterMetadata")

@_attrs_define
class ClusterVariableSearchQueryRequestFilterMetadata:
    additional_properties: dict[str, AdvancedMetadataValueFilter] = _attrs_field(
        init=False, factory=dict
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> AdvancedMetadataValueFilter: ...
    def __setitem__(self, key: str, value: AdvancedMetadataValueFilter) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
