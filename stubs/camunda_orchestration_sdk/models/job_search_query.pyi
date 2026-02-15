from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.job_search_query_filter import JobSearchQueryFilter
from ..models.job_search_query_sort_request import JobSearchQuerySortRequest
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.offset_based_pagination import OffsetBasedPagination
T = TypeVar("T", bound="JobSearchQuery")
@_attrs_define
class JobSearchQuery:
    sort: list[JobSearchQuerySortRequest] | Unset = UNSET
    filter_: JobSearchQueryFilter | Unset = UNSET
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
