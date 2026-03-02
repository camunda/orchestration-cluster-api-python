from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    IncidentKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_element_id,
    lift_element_instance_key,
    lift_incident_key,
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

from ..models.element_instance_result_state import ElementInstanceResultState
from ..models.element_instance_result_type import ElementInstanceResultType
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ElementInstanceResult")


@_attrs_define
class ElementInstanceResult:
    """
    Attributes:
        process_definition_id (str): The process definition ID associated to this element instance. Example: new-
            account-onboarding-workflow.
        start_date (datetime.datetime): Date when element instance started.
        element_id (str): The element ID for this element instance. Example: Activity_106kosb.
        element_name (str): The element name for this element instance.
        type_ (ElementInstanceResultType): Type of element as defined set of values.
        state (ElementInstanceResultState): State of element instance as defined set of values.
        has_incident (bool): Shows whether this element instance has an incident. If true also an incidentKey is
            provided.
        tenant_id (str): The tenant ID of the incident. Example: customer-service.
        element_instance_key (str): The assigned key, which acts as a unique identifier for this element instance.
            Example: 2251799813686789.
        process_instance_key (str): The process instance key associated to this element instance. Example:
            2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        process_definition_key (str): The process definition key associated to this element instance. Example:
            2251799813686749.
        end_date (datetime.datetime | None | Unset): Date when element instance finished.
        incident_key (None | str | Unset): Incident key associated with this element instance. Example:
            2251799813689432.
    """

    process_definition_id: ProcessDefinitionId
    start_date: datetime.datetime
    element_id: ElementId
    element_name: str
    type_: ElementInstanceResultType
    state: ElementInstanceResultState
    has_incident: bool
    tenant_id: TenantId
    element_instance_key: ElementInstanceKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    end_date: datetime.datetime | None | Unset = UNSET
    incident_key: None | IncidentKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        start_date = self.start_date.isoformat()

        element_id = self.element_id

        element_name = self.element_name

        type_ = self.type_.value

        state = self.state.value

        has_incident = self.has_incident

        tenant_id = self.tenant_id

        element_instance_key = self.element_instance_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_definition_key = self.process_definition_key

        end_date: None | str | Unset
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        incident_key: None | IncidentKey | Unset
        if isinstance(self.incident_key, Unset):
            incident_key = UNSET
        else:
            incident_key = self.incident_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "startDate": start_date,
                "elementId": element_id,
                "elementName": element_name,
                "type": type_,
                "state": state,
                "hasIncident": has_incident,
                "tenantId": tenant_id,
                "elementInstanceKey": element_instance_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "processDefinitionKey": process_definition_key,
            }
        )
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if incident_key is not UNSET:
            field_dict["incidentKey"] = incident_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        start_date = isoparse(d.pop("startDate"))

        element_id = lift_element_id(d.pop("elementId"))

        element_name = d.pop("elementName")

        type_ = ElementInstanceResultType(d.pop("type"))

        state = ElementInstanceResultState(d.pop("state"))

        has_incident = d.pop("hasIncident")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        element_instance_key = lift_element_instance_key(d.pop("elementInstanceKey"))

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

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

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        def _parse_end_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_date = _parse_end_date(d.pop("endDate", UNSET))

        def _parse_incident_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_incident_key = _parse_incident_key(d.pop("incidentKey", UNSET))

        incident_key = (
            lift_incident_key(_raw_incident_key)
            if isinstance(_raw_incident_key, str)
            else _raw_incident_key
        )

        element_instance_result = cls(
            process_definition_id=process_definition_id,
            start_date=start_date,
            element_id=element_id,
            element_name=element_name,
            type_=type_,
            state=state,
            has_incident=has_incident,
            tenant_id=tenant_id,
            element_instance_key=element_instance_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            process_definition_key=process_definition_key,
            end_date=end_date,
            incident_key=incident_key,
        )

        element_instance_result.additional_properties = d
        return element_instance_result

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
