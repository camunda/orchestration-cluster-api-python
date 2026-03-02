from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.process_element_statistics_result import (
        ProcessElementStatisticsResult,
    )


T = TypeVar("T", bound="ProcessInstanceElementStatisticsQueryResult")


@_attrs_define
class ProcessInstanceElementStatisticsQueryResult:
    """Process instance element statistics query response.

    Attributes:
        items (list[ProcessElementStatisticsResult]): The element statistics.
    """

    items: list[ProcessElementStatisticsResult]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        items: list[dict[str, Any]] = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_element_statistics_result import (
            ProcessElementStatisticsResult,
        )

        d = dict(src_dict)
        items: list[ProcessElementStatisticsResult] = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ProcessElementStatisticsResult.from_dict(items_item_data)

            items.append(items_item)

        process_instance_element_statistics_query_result = cls(
            items=items,
        )

        process_instance_element_statistics_query_result.additional_properties = d
        return process_instance_element_statistics_query_result

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
