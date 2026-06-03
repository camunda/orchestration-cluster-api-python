from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.wait_state_element_type_exact_match import WaitStateElementTypeExactMatch
from ..models.wait_state_type_exact_match import WaitStateTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_element_id_filter import AdvancedElementIdFilter
from ..models.advanced_element_instance_key_filter import AdvancedElementInstanceKeyFilter
from ..models.advanced_process_instance_key_filter import AdvancedProcessInstanceKeyFilter
from ..models.advanced_wait_state_element_type_filter import AdvancedWaitStateElementTypeFilter
from ..models.advanced_wait_state_type_filter import AdvancedWaitStateTypeFilter
T = TypeVar("T", bound="ElementInstanceWaitStateQueryFilter")
@_attrs_define
class ElementInstanceWaitStateQueryFilter:
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    root_process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    element_type: (
            AdvancedWaitStateElementTypeFilter | Unset | WaitStateElementTypeExactMatch
        ) = UNSET
    wait_state_type: AdvancedWaitStateTypeFilter | Unset | WaitStateTypeExactMatch = (
            UNSET
        )
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
