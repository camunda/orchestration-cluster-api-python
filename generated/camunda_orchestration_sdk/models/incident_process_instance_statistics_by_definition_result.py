from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionId,
    ProcessDefinitionKey,
    TenantId,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="IncidentProcessInstanceStatisticsByDefinitionResult")


@_attrs_define
class IncidentProcessInstanceStatisticsByDefinitionResult:
    """
    Attributes:
        process_definition_id (str): Id of a process definition, from the model. Only ids of process definitions that
            are deployed are useful. Example: new-account-onboarding-workflow.
        process_definition_key (str): System-generated key for a deployed process definition. Example: 2251799813686749.
        process_definition_name (str): The name of the process definition.
        process_definition_version (int): The version of the process definition.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        active_instances_with_error_count (int): The number of active process instances that currently have an incident
            with the specified error hash code.
    """

    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_definition_name: str
    process_definition_version: int
    tenant_id: TenantId
    active_instances_with_error_count: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        process_definition_key = self.process_definition_key

        process_definition_name = self.process_definition_name

        process_definition_version = self.process_definition_version

        tenant_id = self.tenant_id

        active_instances_with_error_count = self.active_instances_with_error_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processDefinitionName": process_definition_name,
                "processDefinitionVersion": process_definition_version,
                "tenantId": tenant_id,
                "activeInstancesWithErrorCount": active_instances_with_error_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_definition_name = d.pop("processDefinitionName")

        process_definition_version = d.pop("processDefinitionVersion")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        active_instances_with_error_count = d.pop("activeInstancesWithErrorCount")

        incident_process_instance_statistics_by_definition_result = cls(
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_definition_name=process_definition_name,
            process_definition_version=process_definition_version,
            tenant_id=tenant_id,
            active_instances_with_error_count=active_instances_with_error_count,
        )

        incident_process_instance_statistics_by_definition_result.additional_properties = d
        return incident_process_instance_statistics_by_definition_result

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
