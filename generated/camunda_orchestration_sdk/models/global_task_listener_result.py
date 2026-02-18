from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.global_listener_source_enum import GlobalListenerSourceEnum
from ..models.global_task_listener_event_type_enum import (
    GlobalTaskListenerEventTypeEnum,
)
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="GlobalTaskListenerResult")


@_attrs_define
class GlobalTaskListenerResult:
    """
    Attributes:
        id (str | Unset): The user-defined id for the global listener Example: GlobalListener_1.
        source (GlobalListenerSourceEnum | Unset): How the global listener was defined.
        event_types (list[GlobalTaskListenerEventTypeEnum] | Unset): List of user task event types that trigger the
            listener.
        type_ (str | Unset): The name of the job type, used as a reference to specify which job workers request the
            respective listener job. Example: order-items.
        retries (int | Unset): Number of retries for the listener job.
        after_non_global (bool | Unset): Whether the listener should run after model-level listeners.
        priority (int | Unset): The priority of the listener. Higher priority listeners are executed before lower
            priority ones.
    """

    id: str | Unset = UNSET
    source: GlobalListenerSourceEnum | Unset = UNSET
    event_types: list[GlobalTaskListenerEventTypeEnum] | Unset = UNSET
    type_: str | Unset = UNSET
    retries: int | Unset = UNSET
    after_non_global: bool | Unset = UNSET
    priority: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        event_types: list[str] | Unset = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = []
            for (
                componentsschemas_global_task_listener_event_types_item_data
            ) in self.event_types:
                componentsschemas_global_task_listener_event_types_item = (
                    componentsschemas_global_task_listener_event_types_item_data.value
                )
                event_types.append(
                    componentsschemas_global_task_listener_event_types_item
                )

        type_ = self.type_

        retries = self.retries

        after_non_global = self.after_non_global

        priority = self.priority

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if source is not UNSET:
            field_dict["source"] = source
        if event_types is not UNSET:
            field_dict["eventTypes"] = event_types
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
        id = d.pop("id", UNSET)

        _source = d.pop("source", UNSET)
        source: GlobalListenerSourceEnum | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = GlobalListenerSourceEnum(_source)

        _event_types = d.pop("eventTypes", UNSET)
        event_types: list[GlobalTaskListenerEventTypeEnum] | Unset = UNSET
        if _event_types is not UNSET:
            event_types = []
            for (
                componentsschemas_global_task_listener_event_types_item_data
            ) in _event_types:
                componentsschemas_global_task_listener_event_types_item = (
                    GlobalTaskListenerEventTypeEnum(
                        componentsschemas_global_task_listener_event_types_item_data
                    )
                )

                event_types.append(
                    componentsschemas_global_task_listener_event_types_item
                )

        type_ = d.pop("type", UNSET)

        retries = d.pop("retries", UNSET)

        after_non_global = d.pop("afterNonGlobal", UNSET)

        priority = d.pop("priority", UNSET)

        global_task_listener_result = cls(
            id=id,
            source=source,
            event_types=event_types,
            type_=type_,
            retries=retries,
            after_non_global=after_non_global,
            priority=priority,
        )

        global_task_listener_result.additional_properties = d
        return global_task_listener_result

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
