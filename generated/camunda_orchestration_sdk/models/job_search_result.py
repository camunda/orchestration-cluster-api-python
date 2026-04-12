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

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_kind_enum import JobKindEnum
from ..models.job_listener_event_type_enum import JobListenerEventTypeEnum
from ..models.job_state_enum import JobStateEnum

if TYPE_CHECKING:
    from ..models.job_search_result_custom_headers import JobSearchResultCustomHeaders


T = TypeVar("T", bound="JobSearchResult")


@_attrs_define
class JobSearchResult:
    """
    Attributes:
        custom_headers (JobSearchResultCustomHeaders): A set of custom headers defined during modelling.
        deadline (datetime.datetime | None): If the job has been activated, when it will next be available to be
            activated.
        denied_reason (None | str): The reason provided by the user task listener for denying the work.
        element_id (None | str): The element ID associated with the job. May be missing on job failure. Example:
            Activity_106kosb.
        element_instance_key (str): The element instance key associated with the job. Example: 2251799813686789.
        end_time (datetime.datetime | None): End date of the job.
            This is `null` if the job is not in an end state yet.
        error_code (None | str): The error code provided for a failed job.
        error_message (None | str): The error message that provides additional context for a failed job.
        has_failed_with_retries_left (bool): Indicates whether the job has failed with retries left.
        is_denied (bool | None): Indicates whether the user task listener denies the work.
        job_key (str): The key, a unique identifier for the job. Example: 2251799813653498.
        kind (JobKindEnum): The job kind. Example: BPMN_ELEMENT.
        listener_event_type (JobListenerEventTypeEnum): The listener event type of the job. Example: UNSPECIFIED.
        process_definition_id (str): The process definition ID associated with the job. Example: new-account-onboarding-
            workflow.
        process_definition_key (str): The process definition key associated with the job. Example: 2251799813686749.
        process_instance_key (str): The process instance key associated with the job. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        retries (int): The amount of retries left to this job.
        state (JobStateEnum): The state of the job.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        type_ (str): The type of the job.
        worker (str): The name of the worker of this job.
        creation_time (datetime.datetime | None): When the job was created. Field is present for jobs created after 8.9.
        last_update_time (datetime.datetime | None): When the job was last updated. Field is present for jobs created
            after 8.9.
    """

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
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        custom_headers = self.custom_headers.to_dict()

        deadline: None | str
        if isinstance(self.deadline, datetime.datetime):
            deadline = self.deadline.isoformat()
        else:
            deadline = self.deadline

        denied_reason: None | str
        denied_reason = self.denied_reason

        element_id: None | ElementId
        element_id = self.element_id

        element_instance_key = self.element_instance_key

        end_time: None | str
        if isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        error_code: None | str
        error_code = self.error_code

        error_message: None | str
        error_message = self.error_message

        has_failed_with_retries_left = self.has_failed_with_retries_left

        is_denied: bool | None
        is_denied = self.is_denied

        job_key = self.job_key

        kind = self.kind.value

        listener_event_type = self.listener_event_type.value

        process_definition_id = self.process_definition_id

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        retries = self.retries

        state = self.state.value

        tenant_id = self.tenant_id

        type_ = self.type_

        worker = self.worker

        creation_time: None | str
        if isinstance(self.creation_time, datetime.datetime):
            creation_time = self.creation_time.isoformat()
        else:
            creation_time = self.creation_time

        last_update_time: None | str
        if isinstance(self.last_update_time, datetime.datetime):
            last_update_time = self.last_update_time.isoformat()
        else:
            last_update_time = self.last_update_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customHeaders": custom_headers,
                "deadline": deadline,
                "deniedReason": denied_reason,
                "elementId": element_id,
                "elementInstanceKey": element_instance_key,
                "endTime": end_time,
                "errorCode": error_code,
                "errorMessage": error_message,
                "hasFailedWithRetriesLeft": has_failed_with_retries_left,
                "isDenied": is_denied,
                "jobKey": job_key,
                "kind": kind,
                "listenerEventType": listener_event_type,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "retries": retries,
                "state": state,
                "tenantId": tenant_id,
                "type": type_,
                "worker": worker,
                "creationTime": creation_time,
                "lastUpdateTime": last_update_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_search_result_custom_headers import (
            JobSearchResultCustomHeaders,
        )

        d = dict(src_dict)
        custom_headers = JobSearchResultCustomHeaders.from_dict(d.pop("customHeaders"))

        def _parse_deadline(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deadline_type_0 = isoparse(data)

                return deadline_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        deadline = _parse_deadline(d.pop("deadline"))

        def _parse_denied_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        denied_reason = _parse_denied_reason(d.pop("deniedReason"))

        def _parse_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_id = _parse_element_id(d.pop("elementId"))

        element_id = (
            ElementId(_raw_element_id)
            if isinstance(_raw_element_id, str)
            else _raw_element_id
        )

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        def _parse_end_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end_time = _parse_end_time(d.pop("endTime"))

        def _parse_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_code = _parse_error_code(d.pop("errorCode"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))

        has_failed_with_retries_left = d.pop("hasFailedWithRetriesLeft")

        def _parse_is_denied(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        is_denied = _parse_is_denied(d.pop("isDenied"))

        job_key = JobKey(d.pop("jobKey"))

        kind = JobKindEnum(d.pop("kind"))

        listener_event_type = JobListenerEventTypeEnum(d.pop("listenerEventType"))

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        retries = d.pop("retries")

        state = JobStateEnum(d.pop("state"))

        tenant_id = TenantId(d.pop("tenantId"))

        type_ = d.pop("type")

        worker = d.pop("worker")

        def _parse_creation_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                creation_time_type_0 = isoparse(data)

                return creation_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        creation_time = _parse_creation_time(d.pop("creationTime"))

        def _parse_last_update_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_time_type_0 = isoparse(data)

                return last_update_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_update_time = _parse_last_update_time(d.pop("lastUpdateTime"))

        job_search_result = cls(
            custom_headers=custom_headers,
            deadline=deadline,
            denied_reason=denied_reason,
            element_id=element_id,
            element_instance_key=element_instance_key,
            end_time=end_time,
            error_code=error_code,
            error_message=error_message,
            has_failed_with_retries_left=has_failed_with_retries_left,
            is_denied=is_denied,
            job_key=job_key,
            kind=kind,
            listener_event_type=listener_event_type,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            retries=retries,
            state=state,
            tenant_id=tenant_id,
            type_=type_,
            worker=worker,
            creation_time=creation_time,
            last_update_time=last_update_time,
        )

        job_search_result.additional_properties = d
        return job_search_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
