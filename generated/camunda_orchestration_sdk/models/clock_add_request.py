from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ClockAddRequest")


@_attrs_define
class ClockAddRequest:
    """
    Attributes:
        offset (str): The time to add to the clock, as an ISO 8601 duration in days, hours, minutes, and
            seconds (for example `PT1H` for one hour or `P1D` for one day). Use a negative
            duration such as `-PT1H` to move the clock backward. The request is rejected if the
            new time would be before 1970-01-01T00:00:00Z.
             Example: PT1H.
    """

    offset: str

    def to_dict(self) -> dict[str, Any]:
        offset = self.offset

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        offset = d.pop_required("offset")

        clock_add_request = cls(
            offset=offset,
        )

        return clock_add_request
