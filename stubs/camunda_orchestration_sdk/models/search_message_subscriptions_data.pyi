from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.message_subscription_search_query_filter import MessageSubscriptionSearchQueryFilter
from ..models.message_subscription_search_query_sort_request import MessageSubscriptionSearchQuerySortRequest
from ..models.offset_based_pagination import OffsetBasedPagination
from ..models.page_cursor_based_backward_pagination import PageCursorBasedBackwardPagination
T = TypeVar("T", bound="SearchMessageSubscriptionsData")
@_attrs_define
class SearchMessageSubscriptionsData:
    sort: list[MessageSubscriptionSearchQuerySortRequest] | Unset = UNSET
    filter_: MessageSubscriptionSearchQueryFilter | Unset = UNSET
    page: (
            CursorBasedForwardPagination
            | LimitBasedPagination
            | OffsetBasedPagination
            | PageCursorBasedBackwardPagination
            | Unset
        ) = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
