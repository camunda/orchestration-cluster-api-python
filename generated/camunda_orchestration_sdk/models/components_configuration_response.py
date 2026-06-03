from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.webapp_component import WebappComponent

T = TypeVar("T", bound="ComponentsConfigurationResponse")


@_attrs_define
class ComponentsConfigurationResponse:
    """Configuration for active Camunda components in the deployment.

    Attributes:
        active (list[WebappComponent]): List of webapp components whose UI is enabled in this deployment. Example:
            ['operate', 'tasklist'].
    """

    active: list[WebappComponent]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        active: list[Any] = []
        for active_item_data in self.active:
            active_item = active_item_data.value
            active.append(active_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active: list[WebappComponent] = []
        _active = d.pop("active")
        for active_item_data in _active:
            active_item = WebappComponent(active_item_data)

            active.append(active_item)

        components_configuration_response = cls(
            active=active,
        )

        components_configuration_response.additional_properties = d
        return components_configuration_response

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
