from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.authorization_id_based_request_permission_types_item import (
    AuthorizationIdBasedRequestPermissionTypesItem,
)
from ..models.authorization_id_based_request_resource_type import (
    AuthorizationIdBasedRequestResourceType,
)
from ..models.owner_type_enum import OwnerTypeEnum

T = TypeVar("T", bound="AuthorizationIdBasedRequest")


@_attrs_define
class AuthorizationIdBasedRequest:
    """
    Attributes:
        owner_id (str): The ID of the owner of the permissions.
        owner_type (OwnerTypeEnum): The type of the owner of permissions.
        resource_id (str): The ID of the resource to add permissions to.
        resource_type (AuthorizationIdBasedRequestResourceType): The type of resource to add permissions to.
        permission_types (list[AuthorizationIdBasedRequestPermissionTypesItem]): The permission types to add.
    """

    owner_id: str
    owner_type: OwnerTypeEnum
    resource_id: str
    resource_type: AuthorizationIdBasedRequestResourceType
    permission_types: list[AuthorizationIdBasedRequestPermissionTypesItem]

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        owner_type = self.owner_type.value

        resource_id = self.resource_id

        resource_type = self.resource_type.value

        permission_types: list[Any] = []
        for permission_types_item_data in self.permission_types:
            permission_types_item = permission_types_item_data.value
            permission_types.append(permission_types_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ownerId": owner_id,
                "ownerType": owner_type,
                "resourceId": resource_id,
                "resourceType": resource_type,
                "permissionTypes": permission_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId")

        owner_type = OwnerTypeEnum(d.pop("ownerType"))

        resource_id = d.pop("resourceId")

        resource_type = AuthorizationIdBasedRequestResourceType(d.pop("resourceType"))

        permission_types: list[AuthorizationIdBasedRequestPermissionTypesItem] = []
        _permission_types = d.pop("permissionTypes")
        for permission_types_item_data in _permission_types:
            permission_types_item = AuthorizationIdBasedRequestPermissionTypesItem(
                permission_types_item_data
            )

            permission_types.append(permission_types_item)

        authorization_id_based_request = cls(
            owner_id=owner_id,
            owner_type=owner_type,
            resource_id=resource_id,
            resource_type=resource_type,
            permission_types=permission_types,
        )

        return authorization_id_based_request
