from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceResult")


@_attrs_define
class ResourceResult:
    """
    Attributes:
        resource_name (str): The resource name from which this resource was parsed.
        version (int): The assigned resource version.
        version_tag (None | str): The version tag of this resource.
        resource_id (str): The resource ID of this resource.
        tenant_id (str): The tenant ID of this resource. Example: customer-service.
        resource_key (str): The unique key of this resource.
    """

    resource_name: str
    version: int
    version_tag: None | str
    resource_id: str
    tenant_id: TenantId
    resource_key: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        resource_name = self.resource_name

        version = self.version

        version_tag: None | str
        version_tag = self.version_tag

        resource_id = self.resource_id

        tenant_id = self.tenant_id

        resource_key: str
        resource_key = self.resource_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceName": resource_name,
                "version": version,
                "versionTag": version_tag,
                "resourceId": resource_id,
                "tenantId": tenant_id,
                "resourceKey": resource_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_name = d.pop("resourceName")

        version = d.pop("version")

        def _parse_version_tag(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        version_tag = _parse_version_tag(d.pop("versionTag"))

        resource_id = d.pop("resourceId")

        tenant_id = TenantId(d.pop("tenantId"))

        def _parse_resource_key(data: object) -> str:
            return cast(str, data)

        resource_key = _parse_resource_key(d.pop("resourceKey"))

        resource_result = cls(
            resource_name=resource_name,
            version=version,
            version_tag=version_tag,
            resource_id=resource_id,
            tenant_id=tenant_id,
            resource_key=resource_key,
        )

        resource_result.additional_properties = d
        return resource_result

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
