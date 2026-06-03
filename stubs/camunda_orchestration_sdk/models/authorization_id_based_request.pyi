from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.authorization_id_based_request_permission_types_item import AuthorizationIdBasedRequestPermissionTypesItem
from ..models.authorization_id_based_request_resource_type import AuthorizationIdBasedRequestResourceType
from ..models.owner_type_enum import OwnerTypeEnum
T = TypeVar("T", bound="AuthorizationIdBasedRequest")
@_attrs_define
class AuthorizationIdBasedRequest:
    owner_id: str
    owner_type: OwnerTypeEnum
    resource_id: str
    resource_type: AuthorizationIdBasedRequestResourceType
    permission_types: list[AuthorizationIdBasedRequestPermissionTypesItem]
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
