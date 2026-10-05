from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="TimerWaitStateDetails")


@_attrs_define
class TimerWaitStateDetails:
    """
    Attributes:
        due_date (int | None): When the timer is due, as a UNIX epoch timestamp in milliseconds.
        repetitions (int | None): The number of remaining timer repetitions (-1 for infinite, 0 for non-repeating).
        wait_state_type (str): The wait state type discriminator.
    """

    due_date: int | None
    repetitions: int | None
    wait_state_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        due_date: int | None
        due_date = self.due_date

        repetitions: int | None
        repetitions = self.repetitions

        wait_state_type = self.wait_state_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dueDate": due_date,
                "repetitions": repetitions,
                "waitStateType": wait_state_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_due_date(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        due_date = _parse_due_date(d.pop("dueDate"))

        def _parse_repetitions(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        repetitions = _parse_repetitions(d.pop("repetitions"))

        wait_state_type = d.pop("waitStateType")

        timer_wait_state_details = cls(
            due_date=due_date,
            repetitions=repetitions,
            wait_state_type=wait_state_type,
        )

        timer_wait_state_details.additional_properties = d
        return timer_wait_state_details

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
