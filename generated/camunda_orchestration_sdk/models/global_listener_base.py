from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="GlobalListenerBase")


@_attrs_define
class GlobalListenerBase:
    """
    Attributes:
        type_ (str | Unset): The name of the job type, used as a reference to specify which job workers request the
            respective listener job. Example: order-items.
        retries (int | Unset): Number of retries for the listener job.
        after_non_global (bool | Unset): Whether the listener should run after model-level listeners.
        priority (int | Unset): The priority of the listener. Higher priority listeners are executed before lower
            priority ones.
    """

    type_: str | Unset = UNSET
    retries: int | Unset = UNSET
    after_non_global: bool | Unset = UNSET
    priority: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        retries = self.retries

        after_non_global = self.after_non_global

        priority = self.priority

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if retries is not UNSET:
            field_dict["retries"] = retries
        if after_non_global is not UNSET:
            field_dict["afterNonGlobal"] = after_non_global
        if priority is not UNSET:
            field_dict["priority"] = priority

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        retries = d.pop("retries", UNSET)

        after_non_global = d.pop("afterNonGlobal", UNSET)

        priority = d.pop("priority", UNSET)

        global_listener_base = cls(
            type_=type_,
            retries=retries,
            after_non_global=after_non_global,
            priority=priority,
        )

        global_listener_base.additional_properties = d
        return global_listener_base

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
