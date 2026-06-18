from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="SignalWaitStateDetails")


@_attrs_define
class SignalWaitStateDetails:
    """
    Attributes:
        signal_name (str): The name of the signal being awaited.
        wait_state_type (str): The wait state type discriminator.
    """

    signal_name: str
    wait_state_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        signal_name = self.signal_name

        wait_state_type = self.wait_state_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signalName": signal_name,
                "waitStateType": wait_state_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signal_name = d.pop("signalName")

        wait_state_type = d.pop("waitStateType")

        signal_wait_state_details = cls(
            signal_name=signal_name,
            wait_state_type=wait_state_type,
        )

        signal_wait_state_details.additional_properties = d
        return signal_wait_state_details

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
