from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionId, TenantId

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProcessDefinitionInstanceStatisticsResult")


@_attrs_define
class ProcessDefinitionInstanceStatisticsResult:
    """Process definition instance statistics response.

    Attributes:
        process_definition_id (str): Id of a process definition, from the model. Only ids of process definitions that
            are deployed are useful. Example: new-account-onboarding-workflow.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        latest_process_definition_name (None | str): Name of the latest deployed process definition instance version.
        has_multiple_versions (bool): Indicates whether multiple versions of this process definition instance are
            deployed.
        active_instances_without_incident_count (int): Total number of currently active process instances of this
            definition that do not have incidents.
        active_instances_with_incident_count (int): Total number of currently active process instances of this
            definition that have at least one incident.
    """

    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId
    latest_process_definition_name: None | str
    has_multiple_versions: bool
    active_instances_without_incident_count: int
    active_instances_with_incident_count: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        tenant_id = self.tenant_id

        latest_process_definition_name: None | str
        latest_process_definition_name = self.latest_process_definition_name

        has_multiple_versions = self.has_multiple_versions

        active_instances_without_incident_count = (
            self.active_instances_without_incident_count
        )

        active_instances_with_incident_count = self.active_instances_with_incident_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "tenantId": tenant_id,
                "latestProcessDefinitionName": latest_process_definition_name,
                "hasMultipleVersions": has_multiple_versions,
                "activeInstancesWithoutIncidentCount": active_instances_without_incident_count,
                "activeInstancesWithIncidentCount": active_instances_with_incident_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        tenant_id = TenantId(d.pop("tenantId"))

        def _parse_latest_process_definition_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        latest_process_definition_name = _parse_latest_process_definition_name(
            d.pop("latestProcessDefinitionName")
        )

        has_multiple_versions = d.pop("hasMultipleVersions")

        active_instances_without_incident_count = d.pop(
            "activeInstancesWithoutIncidentCount"
        )

        active_instances_with_incident_count = d.pop("activeInstancesWithIncidentCount")

        process_definition_instance_statistics_result = cls(
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
            latest_process_definition_name=latest_process_definition_name,
            has_multiple_versions=has_multiple_versions,
            active_instances_without_incident_count=active_instances_without_incident_count,
            active_instances_with_incident_count=active_instances_with_incident_count,
        )

        process_definition_instance_statistics_result.additional_properties = d
        return process_definition_instance_statistics_result

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
