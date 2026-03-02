from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_global_listener_source_filter_eq import AdvancedGlobalListenerSourceFilterEq
from ..models.advanced_global_listener_source_filter_neq import AdvancedGlobalListenerSourceFilterNeq
from ..models.global_listener_source_enum import GlobalListenerSourceEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="AdvancedGlobalListenerSourceFilter")
@_attrs_define
class AdvancedGlobalListenerSourceFilter:
    eq: AdvancedGlobalListenerSourceFilterEq | Unset = UNSET
    neq: AdvancedGlobalListenerSourceFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[GlobalListenerSourceEnum] | Unset = UNSET
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
