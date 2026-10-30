from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.advanced_protection_mode_filter_eq import AdvancedProtectionModeFilterEq
from ..models.advanced_protection_mode_filter_neq import AdvancedProtectionModeFilterNeq
from ..models.protection_mode_enum import ProtectionModeEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedProtectionModeFilter")


@_attrs_define
class AdvancedProtectionModeFilter:
    """Advanced ProtectionModeEnum filter.

    Attributes:
        eq (AdvancedProtectionModeFilterEq | Unset): Checks if the variable has the provided protection mode.
        neq (AdvancedProtectionModeFilterNeq | Unset): Checks if the variable does not have the provided protection
            mode.
        exists (bool | Unset): Checks if the variable has any protection mode. Use `false` to match the variables
            that are not protected.
        in_ (list[ProtectionModeEnum] | Unset): Checks if the variable has at least one of the provided protection
            modes.
        not_in (list[ProtectionModeEnum] | Unset): Checks if the variable has none of the provided protection modes.
    """

    eq: AdvancedProtectionModeFilterEq | Unset = UNSET
    neq: AdvancedProtectionModeFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[ProtectionModeEnum] | Unset = UNSET
    not_in: list[ProtectionModeEnum] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        eq: str | Unset = UNSET
        if not isinstance(self.eq, Unset):
            eq = self.eq.value

        neq: str | Unset = UNSET
        if not isinstance(self.neq, Unset):
            neq = self.neq.value

        exists = self.exists

        in_: list[str] | Unset = UNSET
        if not isinstance(self.in_, Unset):
            in_ = []
            for in_item_data in self.in_:
                in_item = in_item_data.value
                in_.append(in_item)

        not_in: list[str] | Unset = UNSET
        if not isinstance(self.not_in, Unset):
            not_in = []
            for not_in_item_data in self.not_in:
                not_in_item = not_in_item_data.value
                not_in.append(not_in_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eq is not UNSET:
            field_dict["$eq"] = eq
        if neq is not UNSET:
            field_dict["$neq"] = neq
        if exists is not UNSET:
            field_dict["$exists"] = exists
        if in_ is not UNSET:
            field_dict["$in"] = in_
        if not_in is not UNSET:
            field_dict["$notIn"] = not_in

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _eq = d.pop("$eq", UNSET)
        eq: AdvancedProtectionModeFilterEq | Unset
        if isinstance(_eq, Unset):
            eq = UNSET
        else:
            eq = AdvancedProtectionModeFilterEq(_eq)

        _neq = d.pop("$neq", UNSET)
        neq: AdvancedProtectionModeFilterNeq | Unset
        if isinstance(_neq, Unset):
            neq = UNSET
        else:
            neq = AdvancedProtectionModeFilterNeq(_neq)

        exists = d.pop("$exists", UNSET)

        _in_ = d.pop("$in", UNSET)
        in_: list[ProtectionModeEnum] | Unset = UNSET
        if _in_ is not UNSET:
            in_ = []
            for in_item_data in _in_:
                in_item = ProtectionModeEnum(in_item_data)

                in_.append(in_item)

        _not_in = d.pop("$notIn", UNSET)
        not_in: list[ProtectionModeEnum] | Unset = UNSET
        if _not_in is not UNSET:
            not_in = []
            for not_in_item_data in _not_in:
                not_in_item = ProtectionModeEnum(not_in_item_data)

                not_in.append(not_in_item)

        advanced_protection_mode_filter = cls(
            eq=eq,
            neq=neq,
            exists=exists,
            in_=in_,
            not_in=not_in,
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
