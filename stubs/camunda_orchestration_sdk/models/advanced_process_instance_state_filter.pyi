from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_process_instance_state_filter_eq import AdvancedProcessInstanceStateFilterEq
from ..models.advanced_process_instance_state_filter_neq import AdvancedProcessInstanceStateFilterNeq
from ..models.process_instance_state_enum import ProcessInstanceStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="AdvancedProcessInstanceStateFilter")
@_attrs_define
class AdvancedProcessInstanceStateFilter:
    eq: AdvancedProcessInstanceStateFilterEq | Unset = UNSET
    neq: AdvancedProcessInstanceStateFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[ProcessInstanceStateEnum] | Unset = UNSET
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
