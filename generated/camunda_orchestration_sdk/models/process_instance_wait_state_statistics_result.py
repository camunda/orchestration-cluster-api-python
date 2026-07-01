from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProcessInstanceWaitStateStatisticsResult")


@_attrs_define
class ProcessInstanceWaitStateStatisticsResult:
    """Process instance wait state statistics response item.

    Attributes:
        element_id (str): The element id for which the wait states are aggregated. Example: Activity_106kosb.
        waiting_count (int): The total number of waiting instances of the element.
    """

    element_id: ElementId
    waiting_count: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_id = self.element_id

        waiting_count = self.waiting_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementId": element_id,
                "waitingCount": waiting_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        element_id = ElementId(d.pop("elementId"))

        waiting_count = d.pop("waitingCount")

        process_instance_wait_state_statistics_result = cls(
            element_id=element_id,
            waiting_count=waiting_count,
        )

        process_instance_wait_state_statistics_result.additional_properties = d
        return process_instance_wait_state_statistics_result

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
