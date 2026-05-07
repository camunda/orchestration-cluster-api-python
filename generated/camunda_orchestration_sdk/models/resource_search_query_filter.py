from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="ResourceSearchQueryFilter")


@_attrs_define
class ResourceSearchQueryFilter:
    """The resource search filters.

    Attributes:
        resource_key (AdvancedResourceKeyFilter | str | Unset): The key for this resource.
        resource_name (AdvancedStringFilter | str | Unset): Resource name of this resource.
        resource_id (AdvancedStringFilter | str | Unset): Resource ID of this resource.
        version (AdvancedIntegerFilter | int | Unset): Version of this resource.
        version_tag (AdvancedStringFilter | str | Unset): Version tag of this resource.
        deployment_key (AdvancedDeploymentKeyFilter | str | Unset): Deployment key of this resource.
        tenant_id (str | Unset): Tenant ID of this resource. Example: customer-service.
    """

    resource_key: AdvancedResourceKeyFilter | str | Unset = UNSET
    resource_name: AdvancedStringFilter | str | Unset = UNSET
    resource_id: AdvancedStringFilter | str | Unset = UNSET
    version: AdvancedIntegerFilter | int | Unset = UNSET
    version_tag: AdvancedStringFilter | str | Unset = UNSET
    deployment_key: AdvancedDeploymentKeyFilter | str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        resource_key: dict[str, Any] | str | Unset
        if isinstance(self.resource_key, Unset):
            resource_key = UNSET
        elif isinstance(self.resource_key, AdvancedResourceKeyFilter):
            resource_key = self.resource_key.to_dict()
        else:
            resource_key = self.resource_key

        resource_name: dict[str, Any] | str | Unset
        if isinstance(self.resource_name, Unset):
            resource_name = UNSET
        elif isinstance(self.resource_name, AdvancedStringFilter):
            resource_name = self.resource_name.to_dict()
        else:
            resource_name = self.resource_name

        resource_id: dict[str, Any] | str | Unset
        if isinstance(self.resource_id, Unset):
            resource_id = UNSET
        elif isinstance(self.resource_id, AdvancedStringFilter):
            resource_id = self.resource_id.to_dict()
        else:
            resource_id = self.resource_id

        version: dict[str, Any] | int | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        elif isinstance(self.version, AdvancedIntegerFilter):
            version = self.version.to_dict()
        else:
            version = self.version

        version_tag: dict[str, Any] | str | Unset
        if isinstance(self.version_tag, Unset):
            version_tag = UNSET
        elif isinstance(self.version_tag, AdvancedStringFilter):
            version_tag = self.version_tag.to_dict()
        else:
            version_tag = self.version_tag

        deployment_key: dict[str, Any] | str | Unset
        if isinstance(self.deployment_key, Unset):
            deployment_key = UNSET
        elif isinstance(self.deployment_key, AdvancedDeploymentKeyFilter):
            deployment_key = self.deployment_key.to_dict()
        else:
            deployment_key = self.deployment_key

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resource_key is not UNSET:
            field_dict["resourceKey"] = resource_key
        if resource_name is not UNSET:
            field_dict["resourceName"] = resource_name
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if version is not UNSET:
            field_dict["version"] = version
        if version_tag is not UNSET:
            field_dict["versionTag"] = version_tag
        if deployment_key is not UNSET:
            field_dict["deploymentKey"] = deployment_key
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_resource_key(
            data: object,
        ) -> AdvancedResourceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                resource_key_type_1 = AdvancedResourceKeyFilter.from_dict(data)

                return resource_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedResourceKeyFilter | str | Unset, data)

        resource_key = _parse_resource_key(d.pop("resourceKey", UNSET))

        def _parse_resource_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                resource_name_type_1 = AdvancedStringFilter.from_dict(data)

                return resource_name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        resource_name = _parse_resource_name(d.pop("resourceName", UNSET))

        def _parse_resource_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                resource_id_type_1 = AdvancedStringFilter.from_dict(data)

                return resource_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        resource_id = _parse_resource_id(d.pop("resourceId", UNSET))

        def _parse_version(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                version_type_1 = AdvancedIntegerFilter.from_dict(data)

                return version_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        def _parse_version_tag(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                version_tag_type_1 = AdvancedStringFilter.from_dict(data)

                return version_tag_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        version_tag = _parse_version_tag(d.pop("versionTag", UNSET))

        def _parse_deployment_key(
            data: object,
        ) -> AdvancedDeploymentKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                deployment_key_type_1 = AdvancedDeploymentKeyFilter.from_dict(data)

                return deployment_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDeploymentKeyFilter | str | Unset, data)

        deployment_key = _parse_deployment_key(d.pop("deploymentKey", UNSET))

        tenant_id = TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET

        resource_search_query_filter = cls(
            resource_key=resource_key,
            resource_name=resource_name,
            resource_id=resource_id,
            version=version,
            version_tag=version_tag,
            deployment_key=deployment_key,
            tenant_id=tenant_id,
        )

        resource_search_query_filter.additional_properties = d
        return resource_search_query_filter

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
