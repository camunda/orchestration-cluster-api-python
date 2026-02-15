from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.offset_based_pagination import OffsetBasedPagination
from ..models.page_cursor_based_backward_pagination import PageCursorBasedBackwardPagination
from ..models.tenant_search_query_request_filter import TenantSearchQueryRequestFilter
from ..models.tenant_search_query_sort_request import TenantSearchQuerySortRequest
T = TypeVar("T", bound="SearchTenantsData")
@_attrs_define
class SearchTenantsData:
    sort: list[TenantSearchQuerySortRequest] | Unset = UNSET
    filter_: TenantSearchQueryRequestFilter | Unset = UNSET
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
