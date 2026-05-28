from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cursor_based_backward_pagination import CursorBasedBackwardPagination
    from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
    from ..models.element_instance_wait_state_query_filter import (
        ElementInstanceWaitStateQueryFilter,
    )
    from ..models.limit_based_pagination import LimitBasedPagination
    from ..models.offset_based_pagination import OffsetBasedPagination


T = TypeVar("T", bound="ElementInstanceWaitStateQuery")


@_attrs_define
class ElementInstanceWaitStateQuery:
    """Element instance inspection request.

    Attributes:
        filter_ (ElementInstanceWaitStateQueryFilter | Unset): Filter criteria for the inspection.
        page (CursorBasedBackwardPagination | CursorBasedForwardPagination | LimitBasedPagination |
            OffsetBasedPagination | Unset): Pagination criteria.
    """

    filter_: ElementInstanceWaitStateQueryFilter | Unset = UNSET
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

        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

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
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
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
        from ..models.element_instance_wait_state_query_filter import (
            ElementInstanceWaitStateQueryFilter,
        )
        from ..models.limit_based_pagination import LimitBasedPagination
        from ..models.offset_based_pagination import OffsetBasedPagination

        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: ElementInstanceWaitStateQueryFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = ElementInstanceWaitStateQueryFilter.from_dict(_filter_)

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

        element_instance_wait_state_query = cls(
            filter_=filter_,
            page=page,
        )

        return element_instance_wait_state_query
