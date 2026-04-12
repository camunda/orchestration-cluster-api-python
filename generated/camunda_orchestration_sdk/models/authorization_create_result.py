from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AuthorizationKey

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthorizationCreateResult")


@_attrs_define
class AuthorizationCreateResult:
    """
    Attributes:
        authorization_key (str): The key of the created authorization. Example: 2251799813684332.
    """

    authorization_key: AuthorizationKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        authorization_key = self.authorization_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "authorizationKey": authorization_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        authorization_key = AuthorizationKey(d.pop("authorizationKey"))

        authorization_create_result = cls(
            authorization_key=authorization_key,
        )

        authorization_create_result.additional_properties = d
        return authorization_create_result

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
