from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
from ..models.limit_based_pagination import LimitBasedPagination
from ..models.offset_based_pagination import OffsetBasedPagination
from ..models.user_task_variable_filter import UserTaskVariableFilter
from ..models.variable_search_query_sort_request import VariableSearchQuerySortRequest
T = TypeVar("T", bound="SearchUserTaskVariablesData")
@_attrs_define
class SearchUserTaskVariablesData:
    sort: list[VariableSearchQuerySortRequest] | Unset = UNSET
    filter_: UserTaskVariableFilter | Unset = UNSET
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
