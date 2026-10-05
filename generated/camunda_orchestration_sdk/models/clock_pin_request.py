from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ClockPinRequest")


@_attrs_define
class ClockPinRequest:
    """
    Attributes:
        timestamp (int): The exact time in epoch milliseconds to which the clock should be pinned.
    """

    timestamp: int

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        timestamp = d.pop_required("timestamp")

        clock_pin_request = cls(
            timestamp=timestamp,
        )

        return clock_pin_request
