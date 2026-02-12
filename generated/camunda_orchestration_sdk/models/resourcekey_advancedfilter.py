from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ResourcekeyAdvancedfilter")


@_attrs_define
class ResourcekeyAdvancedfilter:
    """Advanced ResourceKey filter.

    Attributes:
        eq (str | Unset): Checks for equality with the provided value.
        neq (str | Unset): Checks for inequality with the provided value.
        exists (bool | Unset): Checks if the current property exists.
        in_ (list[str] | Unset): Checks if the property matches any of the provided values.
        not_in (list[str] | Unset): Checks if the property matches none of the provided values.
    """

    eq: str | Unset = UNSET
    neq: str | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[str] | Unset = UNSET
    not_in: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        eq: str | Unset
        if isinstance(self.eq, Unset):
            eq = UNSET
        else:
            eq = self.eq

        neq: str | Unset
        if isinstance(self.neq, Unset):
            neq = UNSET
        else:
            neq = self.neq

        exists = self.exists

        in_: list[str] | Unset = UNSET
        if not isinstance(self.in_, Unset):
            in_ = []
            for in_item_data in self.in_:
                in_item: str
                in_item = in_item_data
                in_.append(in_item)

        not_in: list[str] | Unset = UNSET
        if not isinstance(self.not_in, Unset):
            not_in = []
            for not_in_item_data in self.not_in:
                not_in_item: str
                not_in_item = not_in_item_data
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

        def _parse_eq(data: object) -> str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(str | Unset, data)

        eq = _parse_eq(d.pop("$eq", UNSET))

        def _parse_neq(data: object) -> str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(str | Unset, data)

        neq = _parse_neq(d.pop("$neq", UNSET))

        exists = d.pop("$exists", UNSET)

        _in_ = d.pop("$in", UNSET)
        in_: list[str] | Unset = UNSET
        if _in_ is not UNSET:
            in_ = []
            for in_item_data in _in_:

                def _parse_in_item(data: object) -> str:
                    return cast(str, data)

                in_item = _parse_in_item(in_item_data)

                in_.append(in_item)

        _not_in = d.pop("$notIn", UNSET)
        not_in: list[str] | Unset = UNSET
        if _not_in is not UNSET:
            not_in = []
            for not_in_item_data in _not_in:

                def _parse_not_in_item(data: object) -> str:
                    return cast(str, data)

                not_in_item = _parse_not_in_item(not_in_item_data)

                not_in.append(not_in_item)

        resourcekey_advancedfilter = cls(
            eq=eq,
            neq=neq,
            exists=exists,
            in_=in_,
            not_in=not_in,
        )

        resourcekey_advancedfilter.additional_properties = d
        return resourcekey_advancedfilter

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
