from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_task_effective_variable_search_query_request_page import (
        UserTaskEffectiveVariableSearchQueryRequestPage,
    )
    from ..models.user_task_variable_filter import UserTaskVariableFilter
    from ..models.user_task_variable_search_query_sort_request import (
        UserTaskVariableSearchQuerySortRequest,
    )


T = TypeVar("T", bound="UserTaskEffectiveVariableSearchQueryRequest")


@_attrs_define
class UserTaskEffectiveVariableSearchQueryRequest:
    """User task effective variable search query request. Uses offset-based pagination only.

    Attributes:
        page (UserTaskEffectiveVariableSearchQueryRequestPage | Unset): Pagination parameters.
        sort (list[UserTaskVariableSearchQuerySortRequest] | Unset): Sort field criteria.
        filter_ (UserTaskVariableFilter | Unset): The user task variable search filters.
    """

    page: UserTaskEffectiveVariableSearchQueryRequestPage | Unset = UNSET
    sort: list[UserTaskVariableSearchQuerySortRequest] | Unset = UNSET
    filter_: UserTaskVariableFilter | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        page: dict[str, Any] | Unset = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        sort: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()
                sort.append(sort_item)

        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if sort is not UNSET:
            field_dict["sort"] = sort
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_task_effective_variable_search_query_request_page import (
            UserTaskEffectiveVariableSearchQueryRequestPage,
        )
        from ..models.user_task_variable_filter import UserTaskVariableFilter
        from ..models.user_task_variable_search_query_sort_request import (
            UserTaskVariableSearchQuerySortRequest,
        )

        d = dict(src_dict)
        _page = d.pop("page", UNSET)
        page: UserTaskEffectiveVariableSearchQueryRequestPage | Unset
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = UserTaskEffectiveVariableSearchQueryRequestPage.from_dict(_page)

        _sort = d.pop("sort", UNSET)
        sort: list[UserTaskVariableSearchQuerySortRequest] | Unset = UNSET
        if _sort is not UNSET:
            sort = []
            for sort_item_data in _sort:
                sort_item = UserTaskVariableSearchQuerySortRequest.from_dict(
                    sort_item_data
                )

                sort.append(sort_item)

        _filter_ = d.pop("filter", UNSET)
        filter_: UserTaskVariableFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = UserTaskVariableFilter.from_dict(_filter_)

        user_task_effective_variable_search_query_request = cls(
            page=page,
            sort=sort,
            filter_=filter_,
        )

        return user_task_effective_variable_search_query_request
