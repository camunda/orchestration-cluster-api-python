from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.element_instance_wait_state_job_result import (
        ElementInstanceWaitStateJobResult,
    )
    from ..models.element_instance_wait_state_message_result import (
        ElementInstanceWaitStateMessageResult,
    )
    from ..models.search_query_page_response import SearchQueryPageResponse


T = TypeVar("T", bound="ElementInstanceWaitStateQueryResult")


@_attrs_define
class ElementInstanceWaitStateQueryResult:
    """
    Attributes:
        items (list[ElementInstanceWaitStateJobResult | ElementInstanceWaitStateMessageResult]): The matching waiting
            states.
        page (SearchQueryPageResponse): Pagination information about the search results.
    """

    items: list[
        ElementInstanceWaitStateJobResult | ElementInstanceWaitStateMessageResult
    ]
    page: SearchQueryPageResponse
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.element_instance_wait_state_job_result import (
            ElementInstanceWaitStateJobResult,
        )

        items: list[dict[str, Any]] = []
        for items_item_data in self.items:
            items_item: dict[str, Any]
            if isinstance(items_item_data, ElementInstanceWaitStateJobResult):
                items_item = items_item_data.to_dict()
            else:
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
        from ..models.element_instance_wait_state_job_result import (
            ElementInstanceWaitStateJobResult,
        )
        from ..models.element_instance_wait_state_message_result import (
            ElementInstanceWaitStateMessageResult,
        )
        from ..models.search_query_page_response import SearchQueryPageResponse

        d = dict(src_dict)
        items: list[
            ElementInstanceWaitStateJobResult | ElementInstanceWaitStateMessageResult
        ] = []
        _items = d.pop("items")
        for items_item_data in _items:

            def _parse_items_item(
                data: object,
            ) -> (
                ElementInstanceWaitStateJobResult
                | ElementInstanceWaitStateMessageResult
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_element_instance_wait_state_result_type_0 = (
                        ElementInstanceWaitStateJobResult.from_dict(data)
                    )

                    return componentsschemas_element_instance_wait_state_result_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_element_instance_wait_state_result_type_1 = (
                    ElementInstanceWaitStateMessageResult.from_dict(data)
                )

                return componentsschemas_element_instance_wait_state_result_type_1

            items_item = _parse_items_item(items_item_data)

            items.append(items_item)

        page = SearchQueryPageResponse.from_dict(d.pop("page"))

        element_instance_wait_state_query_result = cls(
            items=items,
            page=page,
        )

        element_instance_wait_state_query_result.additional_properties = d
        return element_instance_wait_state_query_result

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
