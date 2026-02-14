from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.audit_log_search_query_sort_request_field import (
    AuditLogSearchQuerySortRequestField,
)
from ..models.sort_order_enum import SortOrderEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditLogSearchQuerySortRequest")


@_attrs_define
class AuditLogSearchQuerySortRequest:
    """
    Attributes:
        field (AuditLogSearchQuerySortRequestField): The field to sort by.
        order (SortOrderEnum | Unset): The order in which to sort the related field.
    """

    field: AuditLogSearchQuerySortRequestField
    order: SortOrderEnum | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field.value

        order: str | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        field_dict: dict[str, Any] = {}

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
        field = AuditLogSearchQuerySortRequestField(d.pop("field"))

        _order = d.pop("order", UNSET)
        order: SortOrderEnum | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = SortOrderEnum(_order)

        audit_log_search_query_sort_request = cls(
            field=field,
            order=order,
        )

        return audit_log_search_query_sort_request
