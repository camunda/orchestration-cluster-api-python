from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.job_kind_enum import JobKindEnum
from ..models.job_listener_event_type_enum import JobListenerEventTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.activated_job_result_custom_headers import ActivatedJobResultCustomHeaders
from ..models.activated_job_result_variables import ActivatedJobResultVariables
from ..models.user_task_properties import UserTaskProperties

T = TypeVar("T", bound="ActivateJobsJobsItem")

@_attrs_define
class ActivateJobsJobsItem:
    type_: str
    process_definition_id: ProcessDefinitionId
    process_definition_version: int
    element_id: ElementId
    custom_headers: ActivatedJobResultCustomHeaders
    worker: str
    retries: int
    deadline: int
    variables: ActivatedJobResultVariables
    tenant_id: TenantId
    job_key: JobKey
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    element_instance_key: ElementInstanceKey
    kind: JobKindEnum
    listener_event_type: JobListenerEventTypeEnum
    user_task: UserTaskProperties | Unset = UNSET
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
