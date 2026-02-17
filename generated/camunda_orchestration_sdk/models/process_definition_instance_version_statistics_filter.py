from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionId,
    TenantId,
    lift_process_definition_id,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ProcessDefinitionInstanceVersionStatisticsFilter")


@_attrs_define
class ProcessDefinitionInstanceVersionStatisticsFilter:
    """Process definition instance version statistics search filter.

    Attributes:
        process_definition_id (str): The ID of the process definition to retrieve version statistics for. Example: new-
            account-onboarding-workflow.
        tenant_id (str | Unset): Tenant ID of this process definition. Example: customer-service.
    """

    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_instance_version_statistics_filter = cls(
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
        )

        process_definition_instance_version_statistics_filter.additional_properties = d
        return process_definition_instance_version_statistics_filter

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
