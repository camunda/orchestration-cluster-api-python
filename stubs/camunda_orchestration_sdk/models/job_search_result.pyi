from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, JobKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.job_kind_enum import JobKindEnum
from ..models.job_listener_event_type_enum import JobListenerEventTypeEnum
from ..models.job_state_enum import JobStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.job_search_result_custom_headers import JobSearchResultCustomHeaders
T = TypeVar("T", bound="JobSearchResult")
@_attrs_define
class JobSearchResult:
    custom_headers: JobSearchResultCustomHeaders
    element_id: ElementId
    element_instance_key: ElementInstanceKey
    has_failed_with_retries_left: bool
    job_key: JobKey
    kind: JobKindEnum
    listener_event_type: JobListenerEventTypeEnum
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    retries: int
    state: JobStateEnum
    tenant_id: TenantId
    type_: str
    worker: str
    deadline: datetime.datetime | None | Unset = UNSET
    denied_reason: None | str | Unset = UNSET
    end_time: datetime.datetime | Unset = UNSET
    error_code: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    is_denied: bool | None | Unset = UNSET
    creation_time: datetime.datetime | Unset = UNSET
    last_update_time: datetime.datetime | Unset = UNSET
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
