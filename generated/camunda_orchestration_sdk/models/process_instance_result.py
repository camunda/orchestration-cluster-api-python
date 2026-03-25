from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BusinessId,
    ElementInstanceKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_business_id,
    lift_element_instance_key,
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

from ..models.process_instance_state_enum import ProcessInstanceStateEnum

T = TypeVar("T", bound="ProcessInstanceResult")


@_attrs_define
class ProcessInstanceResult:
    """Process instance search response item.

    Attributes:
        process_definition_id (str): Id of a process definition, from the model. Only ids of process definitions that
            are deployed are useful. Example: new-account-onboarding-workflow.
        process_definition_name (None | str): The process definition name.
        process_definition_version (int): The process definition version.
        process_definition_version_tag (None | str): The process definition version tag.
        start_date (datetime.datetime): The start time of the process instance.
        end_date (datetime.datetime | None): The completion or termination time of the process instance.
        state (ProcessInstanceStateEnum): Process instance states
        has_incident (bool): Whether this process instance has a related incident or not.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        process_instance_key (str): The key of this process instance. Example: 2251799813690746.
        process_definition_key (str): The process definition key. Example: 2251799813686749.
        parent_process_instance_key (None | str): The parent process instance key. Example: 2251799813690746.
        parent_element_instance_key (None | str): The parent element instance key. Example: 2251799813686789.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        tags (list[str]): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or `.`;
            length ≤ 100. Example: ['high-touch', 'remediation'].
        business_id (None | str): The business id associated with this process instance. Example: order-12345.
    """

    process_definition_id: ProcessDefinitionId
    process_definition_name: None | str
    process_definition_version: int
    process_definition_version_tag: None | str
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    state: ProcessInstanceStateEnum
    has_incident: bool
    tenant_id: TenantId
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    parent_process_instance_key: None | ProcessInstanceKey
    parent_element_instance_key: None | ElementInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    tags: list[str]
    business_id: None | BusinessId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        process_definition_name: None | str
        process_definition_name = self.process_definition_name

        process_definition_version = self.process_definition_version

        process_definition_version_tag: None | str
        process_definition_version_tag = self.process_definition_version_tag

        start_date = self.start_date.isoformat()

        end_date: None | str
        if isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        state = self.state.value

        has_incident = self.has_incident

        tenant_id = self.tenant_id

        process_instance_key = self.process_instance_key

        process_definition_key = self.process_definition_key

        parent_process_instance_key: None | ProcessInstanceKey
        parent_process_instance_key = self.parent_process_instance_key

        parent_element_instance_key: None | ElementInstanceKey
        parent_element_instance_key = self.parent_element_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        tags = self.tags

        business_id: None | BusinessId
        business_id = self.business_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "processDefinitionName": process_definition_name,
                "processDefinitionVersion": process_definition_version,
                "processDefinitionVersionTag": process_definition_version_tag,
                "startDate": start_date,
                "endDate": end_date,
                "state": state,
                "hasIncident": has_incident,
                "tenantId": tenant_id,
                "processInstanceKey": process_instance_key,
                "processDefinitionKey": process_definition_key,
                "parentProcessInstanceKey": parent_process_instance_key,
                "parentElementInstanceKey": parent_element_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "tags": tags,
                "businessId": business_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        def _parse_process_definition_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        process_definition_name = _parse_process_definition_name(
            d.pop("processDefinitionName")
        )

        process_definition_version = d.pop("processDefinitionVersion")

        def _parse_process_definition_version_tag(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        process_definition_version_tag = _parse_process_definition_version_tag(
            d.pop("processDefinitionVersionTag")
        )

        start_date = isoparse(d.pop("startDate"))

        def _parse_end_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end_date = _parse_end_date(d.pop("endDate"))

        state = ProcessInstanceStateEnum(d.pop("state"))

        has_incident = d.pop("hasIncident")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        def _parse_parent_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_parent_process_instance_key = _parse_parent_process_instance_key(
            d.pop("parentProcessInstanceKey")
        )

        parent_process_instance_key = (
            lift_process_instance_key(_raw_parent_process_instance_key)
            if isinstance(_raw_parent_process_instance_key, str)
            else _raw_parent_process_instance_key
        )

        def _parse_parent_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_parent_element_instance_key = _parse_parent_element_instance_key(
            d.pop("parentElementInstanceKey")
        )

        parent_element_instance_key = (
            lift_element_instance_key(_raw_parent_element_instance_key)
            if isinstance(_raw_parent_element_instance_key, str)
            else _raw_parent_element_instance_key
        )

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

        tags = cast(list[str], d.pop("tags"))

        def _parse_business_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_business_id = _parse_business_id(d.pop("businessId"))

        business_id = (
            lift_business_id(_raw_business_id)
            if isinstance(_raw_business_id, str)
            else _raw_business_id
        )

        process_instance_result = cls(
            process_definition_id=process_definition_id,
            process_definition_name=process_definition_name,
            process_definition_version=process_definition_version,
            process_definition_version_tag=process_definition_version_tag,
            start_date=start_date,
            end_date=end_date,
            state=state,
            has_incident=has_incident,
            tenant_id=tenant_id,
            process_instance_key=process_instance_key,
            process_definition_key=process_definition_key,
            parent_process_instance_key=parent_process_instance_key,
            parent_element_instance_key=parent_element_instance_key,
            root_process_instance_key=root_process_instance_key,
            tags=tags,
            business_id=business_id,
        )

        process_instance_result.additional_properties = d
        return process_instance_result

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
