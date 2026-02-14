from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.authorization_filter_resource_type import AuthorizationFilterResourceType
from ..models.owner_type_enum import OwnerTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AuthorizationFilter")


@_attrs_define
class AuthorizationFilter:
    """Authorization search filter.

    Attributes:
        owner_id (str | Unset): The ID of the owner of permissions.
        owner_type (OwnerTypeEnum | Unset): The type of the owner of permissions.
        resource_ids (list[str] | Unset): The IDs of the resource to search permissions for.
        resource_property_names (list[str] | Unset): The names of the resource properties to search permissions for.
        resource_type (AuthorizationFilterResourceType | Unset): The type of resource to search permissions for.
    """

    owner_id: str | Unset = UNSET
    owner_type: OwnerTypeEnum | Unset = UNSET
    resource_ids: list[str] | Unset = UNSET
    resource_property_names: list[str] | Unset = UNSET
    resource_type: AuthorizationFilterResourceType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        owner_id = self.owner_id

        owner_type: str | Unset = UNSET
        if not isinstance(self.owner_type, Unset):
            owner_type = self.owner_type.value

        resource_ids: list[str] | Unset = UNSET
        if not isinstance(self.resource_ids, Unset):
            resource_ids = self.resource_ids

        resource_property_names: list[str] | Unset = UNSET
        if not isinstance(self.resource_property_names, Unset):
            resource_property_names = self.resource_property_names

        resource_type: str | Unset = UNSET
        if not isinstance(self.resource_type, Unset):
            resource_type = self.resource_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if owner_id is not UNSET:
            field_dict["ownerId"] = owner_id
        if owner_type is not UNSET:
            field_dict["ownerType"] = owner_type
        if resource_ids is not UNSET:
            field_dict["resourceIds"] = resource_ids
        if resource_property_names is not UNSET:
            field_dict["resourcePropertyNames"] = resource_property_names
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owner_id = d.pop("ownerId", UNSET)

        _owner_type = d.pop("ownerType", UNSET)
        owner_type: OwnerTypeEnum | Unset
        if isinstance(_owner_type, Unset):
            owner_type = UNSET
        else:
            owner_type = OwnerTypeEnum(_owner_type)

        resource_ids = cast(list[str], d.pop("resourceIds", UNSET))

        resource_property_names = cast(list[str], d.pop("resourcePropertyNames", UNSET))

        _resource_type = d.pop("resourceType", UNSET)
        resource_type: AuthorizationFilterResourceType | Unset
        if isinstance(_resource_type, Unset):
            resource_type = UNSET
        else:
            resource_type = AuthorizationFilterResourceType(_resource_type)

        authorization_filter = cls(
            owner_id=owner_id,
            owner_type=owner_type,
            resource_ids=resource_ids,
            resource_property_names=resource_property_names,
            resource_type=resource_type,
        )

        authorization_filter.additional_properties = d
        return authorization_filter

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
