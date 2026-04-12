from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeploymentResourceResult")


@_attrs_define
class DeploymentResourceResult:
    """A deployed Resource.

    Attributes:
        resource_id (str): The resource id of the deployed resource.
        resource_name (str): The name of the deployed resource.
        version (int): The description of the deployed resource.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        resource_key (str): The assigned key, which acts as a unique identifier for this Resource.
    """

    resource_id: str
    resource_name: str
    version: int
    tenant_id: TenantId
    resource_key: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        resource_id = self.resource_id

        resource_name = self.resource_name

        version = self.version

        tenant_id = self.tenant_id

        resource_key: str
        resource_key = self.resource_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceId": resource_id,
                "resourceName": resource_name,
                "version": version,
                "tenantId": tenant_id,
                "resourceKey": resource_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_id = d.pop("resourceId")

        resource_name = d.pop("resourceName")

        version = d.pop("version")

        tenant_id = TenantId(d.pop("tenantId"))

        def _parse_resource_key(data: object) -> str:
            return cast(str, data)

        resource_key = _parse_resource_key(d.pop("resourceKey"))

        deployment_resource_result = cls(
            resource_id=resource_id,
            resource_name=resource_name,
            version=version,
            tenant_id=tenant_id,
            resource_key=resource_key,
        )

        deployment_resource_result.additional_properties = d
        return deployment_resource_result

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
