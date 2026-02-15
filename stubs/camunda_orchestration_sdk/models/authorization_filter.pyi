from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.authorization_filter_resource_type import AuthorizationFilterResourceType
from ..models.owner_type_enum import OwnerTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="AuthorizationFilter")
@_attrs_define
class AuthorizationFilter:
    owner_id: str | Unset = UNSET
    owner_type: OwnerTypeEnum | Unset = UNSET
    resource_ids: list[str] | Unset = UNSET
    resource_property_names: list[str] | Unset = UNSET
    resource_type: AuthorizationFilterResourceType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
            init=False, factory=str_any_dict_factory
        )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
