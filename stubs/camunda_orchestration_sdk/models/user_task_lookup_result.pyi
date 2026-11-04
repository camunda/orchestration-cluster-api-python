from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    BusinessId,
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
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.user_task_lookup_state_enum import UserTaskLookupStateEnum
from ..models.user_task_lookup_result_variables import UserTaskLookupResultVariables
from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders

T = TypeVar("T", bound="UserTaskLookupResult")

@_attrs_define
class UserTaskLookupResult:
    user_task_key: UserTaskKey
    state: UserTaskLookupStateEnum
    element_id: ElementId
    element_instance_key: ElementInstanceKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_definition_version: int
    tenant_id: TenantId
    assignee: None | str
    candidate_groups: list[str]
    candidate_users: list[str]
    due_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    form_key: None | FormKey
    external_form_reference: None | str
    custom_headers: UserTaskResultCustomHeaders
    priority: int
    tags: list[str]
    business_id: None | BusinessId
    creation_date: datetime.datetime
    variables: UserTaskLookupResultVariables
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
