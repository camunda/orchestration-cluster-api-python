from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, FormKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId, UserTaskKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.user_task_state_enum import UserTaskStateEnum
from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders
T = TypeVar("T", bound="UserTaskResult")
@_attrs_define
class UserTaskResult:
    name: None | str
    state: UserTaskStateEnum
    assignee: None | str
    element_id: ElementId
    candidate_groups: list[str]
    candidate_users: list[str]
    process_definition_id: ProcessDefinitionId
    creation_date: datetime.datetime
    completion_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    due_date: datetime.datetime | None
    tenant_id: TenantId
    external_form_reference: None | str
    process_definition_version: int
    custom_headers: UserTaskResultCustomHeaders
    user_task_key: UserTaskKey
    element_instance_key: ElementInstanceKey
    process_name: None | str
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    form_key: None | FormKey
    tags: list[str]
    priority: int = 50
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
