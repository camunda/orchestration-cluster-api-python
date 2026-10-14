from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthenticationConfigurationResponse")


@_attrs_define
class AuthenticationConfigurationResponse:
    """Configuration for authentication and session management.

    Attributes:
        can_logout (bool): Whether users can log out (false for SaaS deployments). Example: True.
        is_login_delegated (bool): Whether login is delegated to an external identity provider.
        is_camunda_groups_enabled (bool): Whether Camunda manages group membership locally, as opposed to delegating it
            to the identity provider via a groups claim. Example: True.
    """

    can_logout: bool
    is_login_delegated: bool
    is_camunda_groups_enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        can_logout = self.can_logout

        is_login_delegated = self.is_login_delegated

        is_camunda_groups_enabled = self.is_camunda_groups_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "canLogout": can_logout,
                "isLoginDelegated": is_login_delegated,
                "isCamundaGroupsEnabled": is_camunda_groups_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        can_logout = d.pop_required("canLogout")

        is_login_delegated = d.pop_required("isLoginDelegated")

        is_camunda_groups_enabled = d.pop_required("isCamundaGroupsEnabled")

        authentication_configuration_response = cls(
            can_logout=can_logout,
            is_login_delegated=is_login_delegated,
            is_camunda_groups_enabled=is_camunda_groups_enabled,
        )

        authentication_configuration_response.additional_properties = d
        return authentication_configuration_response

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
