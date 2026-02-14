from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
    from ..models.process_definition_message_subscription_statistics_query_filter import (
        ProcessDefinitionMessageSubscriptionStatisticsQueryFilter,
    )


T = TypeVar("T", bound="ProcessDefinitionMessageSubscriptionStatisticsQuery")


@_attrs_define
class ProcessDefinitionMessageSubscriptionStatisticsQuery:
    """
    Attributes:
        page (CursorBasedForwardPagination | Unset):
        filter_ (ProcessDefinitionMessageSubscriptionStatisticsQueryFilter | Unset): The message subscription filters.
    """

    page: CursorBasedForwardPagination | Unset = UNSET
    filter_: ProcessDefinitionMessageSubscriptionStatisticsQueryFilter | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        page: dict[str, Any] | Unset = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cursor_based_forward_pagination import (
            CursorBasedForwardPagination,
        )
        from ..models.process_definition_message_subscription_statistics_query_filter import (
            ProcessDefinitionMessageSubscriptionStatisticsQueryFilter,
        )

        d = dict(src_dict)
        _page = d.pop("page", UNSET)
        page: CursorBasedForwardPagination | Unset
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = CursorBasedForwardPagination.from_dict(_page)

        _filter_ = d.pop("filter", UNSET)
        filter_: ProcessDefinitionMessageSubscriptionStatisticsQueryFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = (
                ProcessDefinitionMessageSubscriptionStatisticsQueryFilter.from_dict(
                    _filter_
                )
            )

        process_definition_message_subscription_statistics_query = cls(
            page=page,
            filter_=filter_,
        )

        process_definition_message_subscription_statistics_query.additional_properties = d
        return process_definition_message_subscription_statistics_query

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
