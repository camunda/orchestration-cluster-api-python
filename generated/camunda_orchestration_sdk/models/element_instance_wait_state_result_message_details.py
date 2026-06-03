from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ElementInstanceWaitStateResultMessageDetails")


@_attrs_define
class ElementInstanceWaitStateResultMessageDetails:
    """Message details, present when waitStateType is MESSAGE.

    Attributes:
        message_name (str): The name of the message being awaited.
        correlation_key (None | str): The correlation key for the message subscription (null for start events).
    """

    message_name: str
    correlation_key: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        message_name = self.message_name

        correlation_key: None | str
        correlation_key = self.correlation_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messageName": message_name,
                "correlationKey": correlation_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message_name = d.pop("messageName")

        def _parse_correlation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        correlation_key = _parse_correlation_key(d.pop("correlationKey"))

        element_instance_wait_state_result_message_details = cls(
            message_name=message_name,
            correlation_key=correlation_key,
        )

        element_instance_wait_state_result_message_details.additional_properties = d
        return element_instance_wait_state_result_message_details

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
