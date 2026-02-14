from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.audit_log_result import AuditLogResult
    from ..models.search_query_page_response import SearchQueryPageResponse


T = TypeVar("T", bound="AuditLogSearchQueryResult")


@_attrs_define
class AuditLogSearchQueryResult:
    """Audit log search response.

    Attributes:
        page (SearchQueryPageResponse): Pagination information about the search results. Example: {'totalItems': 1,
            'hasMoreTotalItems': False}.
        items (list[AuditLogResult] | Unset): The matching audit logs.
    """

    page: SearchQueryPageResponse
    items: list[AuditLogResult] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        page = self.page.to_dict()

        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
            }
        )
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_log_result import AuditLogResult
        from ..models.search_query_page_response import SearchQueryPageResponse

        d = dict(src_dict)
        page = SearchQueryPageResponse.from_dict(d.pop("page"))

        _items = d.pop("items", UNSET)
        items: list[AuditLogResult] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = AuditLogResult.from_dict(items_item_data)

                items.append(items_item)

        audit_log_search_query_result = cls(
            page=page,
            items=items,
        )

        audit_log_search_query_result.additional_properties = d
        return audit_log_search_query_result

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
