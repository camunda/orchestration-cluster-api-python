from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, FormKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId, UserTaskKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.user_task_state_enum import UserTaskStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders
T = TypeVar("T", bound="UserTaskResult")
@_attrs_define
class UserTaskResult:
    assignee: None | str
    candidate_groups: list[str]
    candidate_users: list[str]
    completion_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    due_date: datetime.datetime | None
    external_form_reference: None | str
    custom_headers: UserTaskResultCustomHeaders
    root_process_instance_key: None | ProcessInstanceKey
    form_key: None | FormKey
    tags: list[str]
    name: str | Unset = UNSET
    state: UserTaskStateEnum | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    creation_date: datetime.datetime | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    process_definition_version: int | Unset = UNSET
    priority: int | Unset = 50
    user_task_key: UserTaskKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    process_name: None | str | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
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
