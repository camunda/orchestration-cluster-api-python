from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    AuthorizationKey,
    lift_authorization_key,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.authorization_result_resource_type import AuthorizationResultResourceType
from ..models.owner_type_enum import OwnerTypeEnum
from ..models.permission_type_enum import PermissionTypeEnum

T = TypeVar("T", bound="AuthorizationResult")


@_attrs_define
class AuthorizationResult:
    """
    Attributes:
        owner_id (str): The ID of the owner of permissions.
        owner_type (OwnerTypeEnum): The type of the owner of permissions.
        resource_type (AuthorizationResultResourceType): The type of resource that the permissions relate to.
        resource_id (None | str): ID of the resource the permission relates to (mutually exclusive with
            `resourcePropertyName`).
        resource_property_name (None | str): The name of the resource property the permission relates to (mutually
            exclusive with `resourceId`).
        permission_types (list[PermissionTypeEnum]): Specifies the types of the permissions.
        authorization_key (str): The key of the authorization. Example: 2251799813684332.
    """

    owner_id: str
    owner_type: OwnerTypeEnum
    resource_type: AuthorizationResultResourceType
    resource_id: None | str
    resource_property_name: None | str
    permission_types: list[PermissionTypeEnum]
    authorization_key: AuthorizationKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        owner_type = self.owner_type.value

        resource_type = self.resource_type.value

        resource_id: None | str
        resource_id = self.resource_id

        resource_property_name: None | str
        resource_property_name = self.resource_property_name

        permission_types: list[Any] = []
        for permission_types_item_data in self.permission_types:
            permission_types_item = permission_types_item_data.value
            permission_types.append(permission_types_item)

        authorization_key = self.authorization_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ownerId": owner_id,
                "ownerType": owner_type,
                "resourceType": resource_type,
                "resourceId": resource_id,
                "resourcePropertyName": resource_property_name,
                "permissionTypes": permission_types,
                "authorizationKey": authorization_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        owner_type = OwnerTypeEnum(d.pop("ownerType"))

        resource_type = AuthorizationResultResourceType(d.pop("resourceType"))

        def _parse_resource_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        resource_id = _parse_resource_id(d.pop("resourceId"))

        def _parse_resource_property_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        resource_property_name = _parse_resource_property_name(
            d.pop("resourcePropertyName")
        )

        permission_types: list[PermissionTypeEnum] = []
        _permission_types = d.pop("permissionTypes")
        for permission_types_item_data in _permission_types:
            permission_types_item = PermissionTypeEnum(permission_types_item_data)

            permission_types.append(permission_types_item)

        authorization_key = lift_authorization_key(d.pop("authorizationKey"))

        authorization_result = cls(
            owner_id=owner_id,
            owner_type=owner_type,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_property_name=resource_property_name,
            permission_types=permission_types,
            authorization_key=authorization_key,
        )

        authorization_result.additional_properties = d
        return authorization_result

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
