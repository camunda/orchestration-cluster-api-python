from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.advanced_global_task_listener_event_type_filter_eq import (
    AdvancedGlobalTaskListenerEventTypeFilterEq,
)
from ..models.advanced_global_task_listener_event_type_filter_neq import (
    AdvancedGlobalTaskListenerEventTypeFilterNeq,
)
from ..models.global_task_listener_event_type_enum import (
    GlobalTaskListenerEventTypeEnum,
)
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedGlobalTaskListenerEventTypeFilter")


@_attrs_define
class AdvancedGlobalTaskListenerEventTypeFilter:
    r"""Advanced global listener event type filter.

    Attributes:
        eq (AdvancedGlobalTaskListenerEventTypeFilterEq | Unset): Checks for equality with the provided value.
        neq (AdvancedGlobalTaskListenerEventTypeFilterNeq | Unset): Checks for inequality with the provided value.
        exists (bool | Unset): Checks if the current property exists.
        in_ (list[GlobalTaskListenerEventTypeEnum] | Unset): Checks if the property matches any of the provided values.
        like (str | Unset): Checks if the property matches the provided like value.

            Supported wildcard characters are:

            * `*`: matches zero, one, or multiple characters.
            * `?`: matches one, single character.

            Wildcard characters can be escaped with backslash, for instance: `\*`.
    """

    eq: AdvancedGlobalTaskListenerEventTypeFilterEq | Unset = UNSET
    neq: AdvancedGlobalTaskListenerEventTypeFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[GlobalTaskListenerEventTypeEnum] | Unset = UNSET
    like: str | Unset = UNSET
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

        like = self.like

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
        if like is not UNSET:
            field_dict["$like"] = like

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _eq = d.pop("$eq", UNSET)
        eq: AdvancedGlobalTaskListenerEventTypeFilterEq | Unset
        if isinstance(_eq, Unset):
            eq = UNSET
        else:
            eq = AdvancedGlobalTaskListenerEventTypeFilterEq(_eq)

        _neq = d.pop("$neq", UNSET)
        neq: AdvancedGlobalTaskListenerEventTypeFilterNeq | Unset
        if isinstance(_neq, Unset):
            neq = UNSET
        else:
            neq = AdvancedGlobalTaskListenerEventTypeFilterNeq(_neq)

        exists = d.pop("$exists", UNSET)

        _in_ = d.pop("$in", UNSET)
        in_: list[GlobalTaskListenerEventTypeEnum] | Unset = UNSET
        if _in_ is not UNSET:
            in_ = []
            for in_item_data in _in_:
                in_item = GlobalTaskListenerEventTypeEnum(in_item_data)

                in_.append(in_item)

        like = d.pop("$like", UNSET)

        advanced_global_task_listener_event_type_filter = cls(
            eq=eq,
            neq=neq,
            exists=exists,
            in_=in_,
            like=like,
        )

        advanced_global_task_listener_event_type_filter.additional_properties = d
        return advanced_global_task_listener_event_type_filter

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
