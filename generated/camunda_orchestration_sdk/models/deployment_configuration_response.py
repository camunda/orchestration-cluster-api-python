from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeploymentConfigurationResponse")


@_attrs_define
class DeploymentConfigurationResponse:
    """Configuration for deployment characteristics.

    Attributes:
        is_enterprise (bool): Whether this is an enterprise deployment.
        is_multi_tenancy_enabled (bool): Whether multi-tenancy is enabled.
        context_path (str): The servlet context path for the deployment.
        max_request_size (int): The maximum HTTP request size in bytes. Example: 4194304.
    """

    is_enterprise: bool
    is_multi_tenancy_enabled: bool
    context_path: str
    max_request_size: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        is_enterprise = self.is_enterprise

        is_multi_tenancy_enabled = self.is_multi_tenancy_enabled

        context_path = self.context_path

        max_request_size = self.max_request_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isEnterprise": is_enterprise,
                "isMultiTenancyEnabled": is_multi_tenancy_enabled,
                "contextPath": context_path,
                "maxRequestSize": max_request_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_enterprise = d.pop("isEnterprise")

        is_multi_tenancy_enabled = d.pop("isMultiTenancyEnabled")

        context_path = d.pop("contextPath")

        max_request_size = d.pop("maxRequestSize")

        deployment_configuration_response = cls(
            is_enterprise=is_enterprise,
            is_multi_tenancy_enabled=is_multi_tenancy_enabled,
            context_path=context_path,
            max_request_size=max_request_size,
        )

        deployment_configuration_response.additional_properties = d
        return deployment_configuration_response

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
