from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    FormKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    UserTaskKey,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.user_task_state_enum import UserTaskStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders

T = TypeVar("T", bound="SearchUserTasksItemsItem")

@_attrs_define
class SearchUserTasksItemsItem:
    name: str | Unset = UNSET
    state: UserTaskStateEnum | Unset = UNSET
    assignee: str | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    candidate_groups: list[str] | Unset = UNSET
    candidate_users: list[str] | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    creation_date: datetime.datetime | Unset = UNSET
    completion_date: datetime.datetime | Unset = UNSET
    follow_up_date: datetime.datetime | Unset = UNSET
    due_date: datetime.datetime | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    external_form_reference: str | Unset = UNSET
    process_definition_version: int | Unset = UNSET
    custom_headers: UserTaskResultCustomHeaders | Unset = UNSET
    priority: int | Unset = 50
    user_task_key: UserTaskKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    process_name: str | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    form_key: FormKey | Unset = UNSET
    tags: list[str] | Unset = UNSET
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
