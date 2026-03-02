from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    EndCursor,
    StartCursor,
    lift_end_cursor,
    lift_start_cursor,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchQueryPageResponse")


@_attrs_define
class SearchQueryPageResponse:
    """Pagination information about the search results.

    Attributes:
        total_items (int): Total items matching the criteria.
        has_more_total_items (bool): Indicates whether there are more items matching the criteria beyond the returned
            items.
            This is useful for determining if additional requests are needed to retrieve all results.
        start_cursor (None | str): The cursor value for getting the previous page of results. Use this in the `before`
            field of an ensuing request. Example: WzIyNTE3OTk4MTM2ODcxMDJd.
        end_cursor (None | str): The cursor value for getting the next page of results. Use this in the `after` field of
            an ensuing request. Example: WzIyNTE3OTk4MTM2ODcxMDJd.
    """

    total_items: int
    has_more_total_items: bool
    start_cursor: None | StartCursor
    end_cursor: None | EndCursor
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        total_items = self.total_items

        has_more_total_items = self.has_more_total_items

        start_cursor: None | StartCursor
        start_cursor = self.start_cursor

        end_cursor: None | EndCursor
        end_cursor = self.end_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalItems": total_items,
                "hasMoreTotalItems": has_more_total_items,
                "startCursor": start_cursor,
                "endCursor": end_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_items = d.pop("totalItems")

        has_more_total_items = d.pop("hasMoreTotalItems")

        def _parse_start_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_start_cursor = _parse_start_cursor(d.pop("startCursor"))

        start_cursor = (
            lift_start_cursor(_raw_start_cursor)
            if isinstance(_raw_start_cursor, str)
            else _raw_start_cursor
        )

        def _parse_end_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_end_cursor = _parse_end_cursor(d.pop("endCursor"))

        end_cursor = (
            lift_end_cursor(_raw_end_cursor)
            if isinstance(_raw_end_cursor, str)
            else _raw_end_cursor
        )

        search_query_page_response = cls(
            total_items=total_items,
            has_more_total_items=has_more_total_items,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
        )

        search_query_page_response.additional_properties = d
        return search_query_page_response

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
