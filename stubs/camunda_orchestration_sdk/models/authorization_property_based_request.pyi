from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.authorization_property_based_request_permission_types_item import (
    AuthorizationPropertyBasedRequestPermissionTypesItem,
)
from ..models.authorization_property_based_request_resource_type import (
    AuthorizationPropertyBasedRequestResourceType,
)
from ..models.owner_type_enum import OwnerTypeEnum

T = TypeVar("T", bound="AuthorizationPropertyBasedRequest")

@_attrs_define
class AuthorizationPropertyBasedRequest:
    owner_id: str
    owner_type: OwnerTypeEnum
    resource_property_name: str
    resource_type: AuthorizationPropertyBasedRequestResourceType
    permission_types: list[AuthorizationPropertyBasedRequestPermissionTypesItem]
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
