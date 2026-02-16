from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, UserTaskKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.user_task_state_exact_match import UserTaskStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_string_filter import AdvancedStringFilter
from ..models.advanced_user_task_state_filter import AdvancedUserTaskStateFilter
from ..models.variable_value_filter_property import VariableValueFilterProperty
T = TypeVar("T", bound="SearchUserTasksFilter")
@_attrs_define
class SearchUserTasksFilter:
    state: AdvancedUserTaskStateFilter | Unset | UserTaskStateExactMatch = UNSET
    assignee: AdvancedStringFilter | str | Unset = UNSET
    priority: AdvancedIntegerFilter | int | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    candidate_group: AdvancedStringFilter | str | Unset = UNSET
    candidate_user: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    creation_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    completion_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    follow_up_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    due_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    process_instance_variables: list[VariableValueFilterProperty] | Unset = UNSET
    local_variables: list[VariableValueFilterProperty] | Unset = UNSET
    user_task_key: UserTaskKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    tags: list[str] | Unset = UNSET
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
