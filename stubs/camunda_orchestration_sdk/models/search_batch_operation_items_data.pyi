from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.batch_operation_item_search_query_sort_request import (
    BatchOperationItemSearchQuerySortRequest,
)
from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.offset_based_pagination import OffsetBasedPagination
from ..models.search_batch_operation_items_filter import SearchBatchOperationItemsFilter

T = TypeVar("T", bound="SearchBatchOperationItemsData")

@_attrs_define
class SearchBatchOperationItemsData:
    sort: list[BatchOperationItemSearchQuerySortRequest] | Unset = UNSET
    filter_: SearchBatchOperationItemsFilter | Unset = UNSET
    page: (
        CursorBasedBackwardPagination
        | CursorBasedForwardPagination
        | LimitBasedPagination
        | OffsetBasedPagination
        | Unset
    ) = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
