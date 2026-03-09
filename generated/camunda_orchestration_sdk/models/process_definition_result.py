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
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProcessDefinitionResult")


@_attrs_define
class ProcessDefinitionResult:
    """
    Attributes:
        name (None | str): Name of this process definition.
        resource_name (str): Resource name for this process definition.
        version (int): Version of this process definition.
        version_tag (None | str): Version tag of this process definition.
        process_definition_id (str): Process definition ID of this process definition. Example: new-account-onboarding-
            workflow.
        tenant_id (str): Tenant ID of this process definition. Example: customer-service.
        process_definition_key (str): The key for this process definition. Example: 2251799813686749.
        has_start_form (bool): Indicates whether the start event of the process has an associated Form Key.
    """

    name: None | str
    resource_name: str
    version: int
    version_tag: None | str
    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId
    process_definition_key: ProcessDefinitionKey
    has_start_form: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        name: None | str
        name = self.name

        resource_name = self.resource_name

        version = self.version

        version_tag: None | str
        version_tag = self.version_tag

        process_definition_id = self.process_definition_id

        tenant_id = self.tenant_id

        process_definition_key = self.process_definition_key

        has_start_form = self.has_start_form

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resourceName": resource_name,
                "version": version,
                "versionTag": version_tag,
                "processDefinitionId": process_definition_id,
                "tenantId": tenant_id,
                "processDefinitionKey": process_definition_key,
                "hasStartForm": has_start_form,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        resource_name = d.pop("resourceName")

        version = d.pop("version")

        def _parse_version_tag(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        version_tag = _parse_version_tag(d.pop("versionTag"))

        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        has_start_form = d.pop("hasStartForm")

        process_definition_result = cls(
            name=name,
            resource_name=resource_name,
            version=version,
            version_tag=version_tag,
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
            process_definition_key=process_definition_key,
            has_start_form=has_start_form,
        )

        process_definition_result.additional_properties = d
        return process_definition_result

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
