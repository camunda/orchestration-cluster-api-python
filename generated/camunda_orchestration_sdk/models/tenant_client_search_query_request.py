from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
    from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
    from ..models.limit_based_pagination import LimitBasedPagination
    from ..models.offset_based_pagination import OffsetBasedPagination
    from ..models.tenant_client_search_query_sort_request import (
        TenantClientSearchQuerySortRequest,
    )


T = TypeVar("T", bound="TenantClientSearchQueryRequest")


@_attrs_define
class TenantClientSearchQueryRequest:
    """
    Attributes:
        sort (list[TenantClientSearchQuerySortRequest] | Unset): Sort field criteria.
        page (CursorBasedBackwardPagination | CursorBasedForwardPagination | LimitBasedPagination |
            OffsetBasedPagination | Unset): Pagination criteria.
    """

    sort: list[TenantClientSearchQuerySortRequest] | Unset = UNSET
    page: (
        CursorBasedBackwardPagination
        | CursorBasedForwardPagination
        | LimitBasedPagination
        | OffsetBasedPagination
        | Unset
    ) = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.cursor_based_forward_pagination import (
            CursorBasedForwardPagination,
        )
        from ..models.limit_based_pagination import LimitBasedPagination
        from ..models.offset_based_pagination import OffsetBasedPagination

        sort: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()
                sort.append(sort_item)

        page: dict[str, Any] | Unset
        if isinstance(self.page, Unset):
            page = UNSET
        elif isinstance(self.page, LimitBasedPagination):
            page = self.page.to_dict()
        elif isinstance(self.page, OffsetBasedPagination):
            page = self.page.to_dict()
        elif isinstance(self.page, CursorBasedForwardPagination):
            page = self.page.to_dict()
        else:
            page = self.page.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if sort is not UNSET:
            field_dict["sort"] = sort
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cursor_based_backward_pagination import (
            CursorBasedBackwardPagination,
        )
        from ..models.cursor_based_forward_pagination import (
            CursorBasedForwardPagination,
        )
        from ..models.limit_based_pagination import LimitBasedPagination
        from ..models.offset_based_pagination import OffsetBasedPagination
        from ..models.tenant_client_search_query_sort_request import (
            TenantClientSearchQuerySortRequest,
        )

        d = dict(src_dict)
        _sort = d.pop("sort", UNSET)
        sort: list[TenantClientSearchQuerySortRequest] | Unset = UNSET
        if _sort is not UNSET:
            sort = []
            for sort_item_data in _sort:
                sort_item = TenantClientSearchQuerySortRequest.from_dict(sort_item_data)

                sort.append(sort_item)

        def _parse_page(
            data: object,
        ) -> (
            CursorBasedBackwardPagination
            | CursorBasedForwardPagination
            | LimitBasedPagination
            | OffsetBasedPagination
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                page_type_0 = LimitBasedPagination.from_dict(data)

                return page_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                page_type_1 = OffsetBasedPagination.from_dict(data)

                return page_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                page_type_2 = CursorBasedForwardPagination.from_dict(data)

                return page_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            page_type_3 = CursorBasedBackwardPagination.from_dict(data)

            return page_type_3

        page = _parse_page(d.pop("page", UNSET))

        tenant_client_search_query_request = cls(
            sort=sort,
            page=page,
        )

        return tenant_client_search_query_request
