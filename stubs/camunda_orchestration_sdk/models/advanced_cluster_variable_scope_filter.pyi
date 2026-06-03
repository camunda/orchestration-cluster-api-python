from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_cluster_variable_scope_filter_eq import AdvancedClusterVariableScopeFilterEq
from ..models.advanced_cluster_variable_scope_filter_neq import AdvancedClusterVariableScopeFilterNeq
from ..models.cluster_variable_scope_enum import ClusterVariableScopeEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="AdvancedClusterVariableScopeFilter")
@_attrs_define
class AdvancedClusterVariableScopeFilter:
    eq: AdvancedClusterVariableScopeFilterEq | Unset = UNSET
    neq: AdvancedClusterVariableScopeFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[ClusterVariableScopeEnum] | Unset = UNSET
    like: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
