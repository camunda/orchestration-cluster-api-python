from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.job_kind_exact_match import JobKindExactMatch
from ..models.job_listener_event_type_exact_match import JobListenerEventTypeExactMatch
from ..models.job_state_exact_match import JobStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_element_instance_key_filter import AdvancedElementInstanceKeyFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
from ..models.advanced_job_kind_filter import AdvancedJobKindFilter
from ..models.advanced_job_listener_event_type_filter import AdvancedJobListenerEventTypeFilter
from ..models.advanced_job_state_filter import AdvancedJobStateFilter
from ..models.advanced_process_definition_key_filter import AdvancedProcessDefinitionKeyFilter
from ..models.advanced_process_instance_key_filter import AdvancedProcessInstanceKeyFilter
from ..models.advanced_string_filter import AdvancedStringFilter
T = TypeVar("T", bound="JobFilter")
@_attrs_define
class JobFilter:
    deadline: AdvancedDateTimeFilter | datetime.datetime | None | Unset = UNSET
    denied_reason: AdvancedStringFilter | str | Unset = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    end_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    error_code: AdvancedStringFilter | str | Unset = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    has_failed_with_retries_left: bool | Unset = UNSET
    is_denied: bool | None | Unset = UNSET
    job_key: AdvancedJobKeyFilter | str | Unset = UNSET
    kind: AdvancedJobKindFilter | JobKindExactMatch | Unset = UNSET
    listener_event_type: (
            AdvancedJobListenerEventTypeFilter | JobListenerEventTypeExactMatch | Unset
        ) = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    retries: AdvancedIntegerFilter | int | Unset = UNSET
    state: AdvancedJobStateFilter | JobStateExactMatch | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    type_: AdvancedStringFilter | str | Unset = UNSET
    worker: AdvancedStringFilter | str | Unset = UNSET
    creation_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    last_update_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
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
