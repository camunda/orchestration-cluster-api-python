from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.protection_mode_enum import ProtectionModeEnum

T = TypeVar("T", bound="VariableSearchResultMetadata")


@_attrs_define
class VariableSearchResultMetadata:
    """Metadata of this variable.

    Attributes:
        protection_modes (list[ProtectionModeEnum]): The protections applied to the variable. The value of a variable
            protected with
            `REDACT` is irrecoverably replaced before it is stored in secondary storage, so it is
            never readable.
    """

    protection_modes: list[ProtectionModeEnum]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        protection_modes: list[Any] = []
        for protection_modes_item_data in self.protection_modes:
            protection_modes_item = protection_modes_item_data.value
            protection_modes.append(protection_modes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protectionModes": protection_modes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        protection_modes: list[ProtectionModeEnum] = []
        _protection_modes = d.pop_required("protectionModes")
        for protection_modes_item_data in _protection_modes:
            protection_modes_item = ProtectionModeEnum(protection_modes_item_data)

            protection_modes.append(protection_modes_item)

        variable_search_result_metadata = cls(
            protection_modes=protection_modes,
        )

        variable_search_result_metadata.additional_properties = d
        return variable_search_result_metadata

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
