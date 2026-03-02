from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    IncidentKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_element_id,
    lift_element_instance_key,
    lift_incident_key,
    lift_job_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.incident_result_error_type import IncidentResultErrorType
from ..models.incident_result_state import IncidentResultState
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="IncidentResult")


@_attrs_define
class IncidentResult:
    """
    Attributes:
        tenant_id (str): The tenant ID of the incident. Example: customer-service.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        job_key (None | str): The job key, if exists, associated with this incident. Example: 2251799813653498.
        process_definition_id (str | Unset): The process definition ID associated to this incident. Example: new-
            account-onboarding-workflow.
        error_type (IncidentResultErrorType | Unset): The type of the incident error.
        error_message (str | Unset): Error message which describes the error in more detail.
        element_id (str | Unset): The element ID associated to this incident. Example: Activity_106kosb.
        creation_time (datetime.datetime | Unset): The creation time of the incident.
        state (IncidentResultState | Unset): The incident state.
        incident_key (str | Unset): The assigned key, which acts as a unique identifier for this incident. Example:
            2251799813689432.
        process_definition_key (str | Unset): The process definition key associated to this incident. Example:
            2251799813686749.
        process_instance_key (str | Unset): The process instance key associated to this incident. Example:
            2251799813690746.
        element_instance_key (str | Unset): The element instance key associated to this incident. Example:
            2251799813686789.
    """

    tenant_id: TenantId
    root_process_instance_key: None | ProcessInstanceKey
    job_key: None | JobKey
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    error_type: IncidentResultErrorType | Unset = UNSET
    error_message: str | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    creation_time: datetime.datetime | Unset = UNSET
    state: IncidentResultState | Unset = UNSET
    incident_key: IncidentKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        job_key: None | JobKey
        job_key = self.job_key

        process_definition_id = self.process_definition_id

        error_type: str | Unset = UNSET
        if not isinstance(self.error_type, Unset):
            error_type = self.error_type.value

        error_message = self.error_message

        element_id = self.element_id

        creation_time: str | Unset = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        state: str | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        incident_key = self.incident_key

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        element_instance_key = self.element_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenantId": tenant_id,
                "rootProcessInstanceKey": root_process_instance_key,
                "jobKey": job_key,
            }
        )
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if error_type is not UNSET:
            field_dict["errorType"] = error_type
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if state is not UNSET:
            field_dict["state"] = state
        if incident_key is not UNSET:
            field_dict["incidentKey"] = incident_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant_id = lift_tenant_id(d.pop("tenantId"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            lift_process_instance_key(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        def _parse_job_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_job_key = _parse_job_key(d.pop("jobKey"))

        job_key = (
            lift_job_key(_raw_job_key)
            if isinstance(_raw_job_key, str)
            else _raw_job_key
        )

        process_definition_id = (
            lift_process_definition_id(_val)
            if (_val := d.pop("processDefinitionId", UNSET)) is not UNSET
            else UNSET
        )

        _error_type = d.pop("errorType", UNSET)
        error_type: IncidentResultErrorType | Unset
        if isinstance(_error_type, Unset):
            error_type = UNSET
        else:
            error_type = IncidentResultErrorType(_error_type)

        error_message = d.pop("errorMessage", UNSET)

        element_id = (
            lift_element_id(_val)
            if (_val := d.pop("elementId", UNSET)) is not UNSET
            else UNSET
        )

        _creation_time = d.pop("creationTime", UNSET)
        creation_time: datetime.datetime | Unset
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        _state = d.pop("state", UNSET)
        state: IncidentResultState | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = IncidentResultState(_state)

        incident_key = (
            lift_incident_key(_val)
            if (_val := d.pop("incidentKey", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_key = (
            lift_process_definition_key(_val)
            if (_val := d.pop("processDefinitionKey", UNSET)) is not UNSET
            else UNSET
        )

        process_instance_key = (
            lift_process_instance_key(_val)
            if (_val := d.pop("processInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        element_instance_key = (
            lift_element_instance_key(_val)
            if (_val := d.pop("elementInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        incident_result = cls(
            tenant_id=tenant_id,
            root_process_instance_key=root_process_instance_key,
            job_key=job_key,
            process_definition_id=process_definition_id,
            error_type=error_type,
            error_message=error_message,
            element_id=element_id,
            creation_time=creation_time,
            state=state,
            incident_key=incident_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
        )

        incident_result.additional_properties = d
        return incident_result

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
