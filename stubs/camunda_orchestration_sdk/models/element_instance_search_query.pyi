from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.element_instance_search_query_filter import (
    ElementInstanceSearchQueryFilter,
)
from ..models.element_instance_search_query_sort_request import (
    ElementInstanceSearchQuerySortRequest,
)
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.offset_based_pagination import OffsetBasedPagination

T = TypeVar("T", bound="ElementInstanceSearchQuery")

@_attrs_define
class ElementInstanceSearchQuery:
    sort: list[ElementInstanceSearchQuerySortRequest] | Unset = UNSET
    filter_: ElementInstanceSearchQueryFilter | Unset = UNSET
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
