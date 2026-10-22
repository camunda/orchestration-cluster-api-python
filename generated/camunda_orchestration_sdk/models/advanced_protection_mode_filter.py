from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.protection_mode_enum import ProtectionModeEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedProtectionModeFilter")


@_attrs_define
class AdvancedProtectionModeFilter:
    """Advanced ProtectionModeEnum filter.

    Attributes:
        in_ (list[ProtectionModeEnum] | Unset): Checks if the variable has at least one of the provided protection
            modes.
    """

    in_: list[ProtectionModeEnum] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        in_: list[str] | Unset = UNSET
        if not isinstance(self.in_, Unset):
            in_ = []
            for in_item_data in self.in_:
                in_item = in_item_data.value
                in_.append(in_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if in_ is not UNSET:
            field_dict["$in"] = in_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _in_ = d.pop("$in", UNSET)
        in_: list[ProtectionModeEnum] | Unset = UNSET
        if _in_ is not UNSET:
            in_ = []
            for in_item_data in _in_:
                in_item = ProtectionModeEnum(in_item_data)

                in_.append(in_item)

        advanced_protection_mode_filter = cls(
            in_=in_,
        )

        advanced_protection_mode_filter.additional_properties = d
        return advanced_protection_mode_filter

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
