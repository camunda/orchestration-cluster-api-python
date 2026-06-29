from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.condition_wait_state_details_events_item import (
    ConditionWaitStateDetailsEventsItem,
)

T = TypeVar("T", bound="ConditionWaitStateDetails")


@_attrs_define
class ConditionWaitStateDetails:
    """
    Attributes:
        expression (str): The condition expression that must evaluate to true to proceed.
        events (list[ConditionWaitStateDetailsEventsItem]): The variable events that trigger condition re-evaluation.
            Empty means all events.
        wait_state_type (str): The wait state type discriminator.
    """

    expression: str
    events: list[ConditionWaitStateDetailsEventsItem]
    wait_state_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        expression = self.expression

        events: list[Any] = []
        for events_item_data in self.events:
            events_item = events_item_data.value
            events.append(events_item)

        wait_state_type = self.wait_state_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expression": expression,
                "events": events,
                "waitStateType": wait_state_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expression = d.pop("expression")

        events: list[ConditionWaitStateDetailsEventsItem] = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = ConditionWaitStateDetailsEventsItem(events_item_data)

            events.append(events_item)

        wait_state_type = d.pop("waitStateType")

        condition_wait_state_details = cls(
            expression=expression,
            events=events,
            wait_state_type=wait_state_type,
        )

        condition_wait_state_details.additional_properties = d
        return condition_wait_state_details

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
