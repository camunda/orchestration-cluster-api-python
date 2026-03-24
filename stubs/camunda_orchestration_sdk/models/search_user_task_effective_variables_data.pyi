from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.user_task_effective_variable_search_query_request_page import UserTaskEffectiveVariableSearchQueryRequestPage
from ..models.user_task_variable_filter import UserTaskVariableFilter
from ..models.variable_search_query_sort_request import VariableSearchQuerySortRequest
T = TypeVar("T", bound="SearchUserTaskEffectiveVariablesData")
@_attrs_define
class SearchUserTaskEffectiveVariablesData:
    page: UserTaskEffectiveVariableSearchQueryRequestPage | Unset = UNSET
    sort: list[VariableSearchQuerySortRequest] | Unset = UNSET
    filter_: UserTaskVariableFilter | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
