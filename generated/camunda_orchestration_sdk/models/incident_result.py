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

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.incident_result_error_type import IncidentResultErrorType
from ..models.incident_result_state import IncidentResultState

T = TypeVar("T", bound="IncidentResult")


@_attrs_define
class IncidentResult:
    """
    Attributes:
        process_definition_id (str): The process definition ID associated to this incident. Example: new-account-
            onboarding-workflow.
        error_type (IncidentResultErrorType): The type of the incident error.
        error_message (str): Error message which describes the error in more detail.
        element_id (str): The element ID associated to this incident. Example: Activity_106kosb.
        creation_time (datetime.datetime): The creation time of the incident.
        state (IncidentResultState): The incident state.
        tenant_id (str): The tenant ID of the incident. Example: customer-service.
        incident_key (str): The assigned key, which acts as a unique identifier for this incident. Example:
            2251799813689432.
        process_definition_key (str): The process definition key associated to this incident. Example: 2251799813686749.
        process_instance_key (str): The process instance key associated to this incident. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        element_instance_key (str): The element instance key associated to this incident. Example: 2251799813686789.
        job_key (None | str): The job key, if exists, associated with this incident. Example: 2251799813653498.
    """

    process_definition_id: ProcessDefinitionId
    error_type: IncidentResultErrorType
    error_message: str
    element_id: ElementId
    creation_time: datetime.datetime
    state: IncidentResultState
    tenant_id: TenantId
    incident_key: IncidentKey
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    job_key: None | JobKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        error_type = self.error_type.value

        error_message = self.error_message

        element_id = self.element_id

        creation_time = self.creation_time.isoformat()

        state = self.state.value

        tenant_id = self.tenant_id

        incident_key = self.incident_key

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        element_instance_key = self.element_instance_key

        job_key: None | JobKey
        job_key = self.job_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "errorType": error_type,
                "errorMessage": error_message,
                "elementId": element_id,
                "creationTime": creation_time,
                "state": state,
                "tenantId": tenant_id,
                "incidentKey": incident_key,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        error_type = IncidentResultErrorType(d.pop("errorType"))

        error_message = d.pop("errorMessage")

        element_id = lift_element_id(d.pop("elementId"))

        creation_time = isoparse(d.pop("creationTime"))

        state = IncidentResultState(d.pop("state"))

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        incident_key = lift_incident_key(d.pop("incidentKey"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = lift_process_instance_key(
            _raw_root_process_instance_key
        )

        element_instance_key = lift_element_instance_key(d.pop("elementInstanceKey"))

        def _parse_job_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_job_key = _parse_job_key(d.pop("jobKey"))

        job_key = lift_job_key(_raw_job_key)

        incident_result = cls(
            process_definition_id=process_definition_id,
            error_type=error_type,
            error_message=error_message,
            element_id=element_id,
            creation_time=creation_time,
            state=state,
            tenant_id=tenant_id,
            incident_key=incident_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            element_instance_key=element_instance_key,
            job_key=job_key,
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
