from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.role_client_result import RoleClientResult
    from ..models.search_query_page_response import SearchQueryPageResponse


T = TypeVar("T", bound="RoleClientSearchResult")


@_attrs_define
class RoleClientSearchResult:
    """
    Attributes:
        items (list[RoleClientResult]): The matching clients.
        page (SearchQueryPageResponse): Pagination information about the search results.
    """

    items: list[RoleClientResult]
    page: SearchQueryPageResponse
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        items: list[dict[str, Any]] = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        page = self.page.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "page": page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_client_result import RoleClientResult
        from ..models.search_query_page_response import SearchQueryPageResponse

        d = dict(src_dict)
        items: list[RoleClientResult] = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RoleClientResult.from_dict(items_item_data)

            items.append(items_item)

        page = SearchQueryPageResponse.from_dict(d.pop("page"))

        role_client_search_result = cls(
            items=items,
            page=page,
        )

        role_client_search_result.additional_properties = d
        return role_client_search_result

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
