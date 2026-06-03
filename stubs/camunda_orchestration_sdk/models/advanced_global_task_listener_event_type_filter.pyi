from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_global_task_listener_event_type_filter_eq import AdvancedGlobalTaskListenerEventTypeFilterEq
from ..models.advanced_global_task_listener_event_type_filter_neq import AdvancedGlobalTaskListenerEventTypeFilterNeq
from ..models.global_task_listener_event_type_enum import GlobalTaskListenerEventTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="AdvancedGlobalTaskListenerEventTypeFilter")
@_attrs_define
class AdvancedGlobalTaskListenerEventTypeFilter:
    eq: AdvancedGlobalTaskListenerEventTypeFilterEq | Unset = UNSET
    neq: AdvancedGlobalTaskListenerEventTypeFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[GlobalTaskListenerEventTypeEnum] | Unset = UNSET
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
