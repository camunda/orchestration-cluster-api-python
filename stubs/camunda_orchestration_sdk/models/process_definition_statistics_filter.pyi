from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.element_instance_state_exact_match import ElementInstanceStateExactMatch
from ..models.process_instance_state_exact_match import ProcessInstanceStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_element_instance_key_filter import AdvancedElementInstanceKeyFilter
from ..models.advanced_element_instance_state_filter import AdvancedElementInstanceStateFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_process_instance_key_filter import AdvancedProcessInstanceKeyFilter
from ..models.advanced_process_instance_state_filter import AdvancedProcessInstanceStateFilter
from ..models.advanced_string_filter import AdvancedStringFilter
from ..models.base_process_instance_filter_fields import BaseProcessInstanceFilterFields
from ..models.variable_value_filter_property import VariableValueFilterProperty
T = TypeVar("T", bound="ProcessDefinitionStatisticsFilter")
@_attrs_define
class ProcessDefinitionStatisticsFilter:
    start_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    end_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    state: (
            AdvancedProcessInstanceStateFilter | ProcessInstanceStateExactMatch | Unset
        ) = UNSET
    has_incident: bool | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    variables: list[VariableValueFilterProperty] | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    parent_process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    parent_element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    batch_operation_id: AdvancedStringFilter | str | Unset = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    has_retries_left: bool | Unset = UNSET
    element_instance_state: (
            AdvancedElementInstanceStateFilter | ElementInstanceStateExactMatch | Unset
        ) = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    has_element_instance_incident: bool | Unset = UNSET
    incident_error_hash_code: AdvancedIntegerFilter | int | Unset = UNSET
    tags: list[str] | Unset = UNSET
    or_: list[BaseProcessInstanceFilterFields] | Unset = UNSET
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
