from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.decision_requirements_search_query_sort_request_field import (
    DecisionRequirementsSearchQuerySortRequestField,
)
from ..models.sort_order_enum import SortOrderEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="DecisionRequirementsSearchQuerySortRequest")


@_attrs_define
class DecisionRequirementsSearchQuerySortRequest:
    """
    Attributes:
        field (DecisionRequirementsSearchQuerySortRequestField): The field to sort by.
        order (SortOrderEnum | Unset): The order in which to sort the related field.
    """

    field: DecisionRequirementsSearchQuerySortRequestField
    order: SortOrderEnum | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        field = self.field.value

        order: str | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
            }
        )
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = DecisionRequirementsSearchQuerySortRequestField(d.pop("field"))

        _order = d.pop("order", UNSET)
        order: SortOrderEnum | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = SortOrderEnum(_order)

        decision_requirements_search_query_sort_request = cls(
            field=field,
            order=order,
        )

        decision_requirements_search_query_sort_request.additional_properties = d
        return decision_requirements_search_query_sort_request

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
