from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, JobKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.job_kind_enum import JobKindEnum
from ..models.job_listener_event_type_enum import JobListenerEventTypeEnum
from ..models.job_state_enum import JobStateEnum
from ..models.job_search_result_custom_headers import JobSearchResultCustomHeaders
T = TypeVar("T", bound="JobSearchResult")
@_attrs_define
class JobSearchResult:
    custom_headers: JobSearchResultCustomHeaders
    deadline: datetime.datetime | None
    denied_reason: None | str
    element_id: None | ElementId
    element_instance_key: ElementInstanceKey
    end_time: datetime.datetime | None
    error_code: None | str
    error_message: None | str
    has_failed_with_retries_left: bool
    is_denied: bool | None
    job_key: JobKey
    kind: JobKindEnum
    listener_event_type: JobListenerEventTypeEnum
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    retries: int
    state: JobStateEnum
    tenant_id: TenantId
    type_: str
    worker: str
    creation_time: datetime.datetime | None
    last_update_time: datetime.datetime | None
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
