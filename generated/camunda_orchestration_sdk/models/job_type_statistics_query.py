from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.cursor_based_forward_pagination import CursorBasedForwardPagination
    from ..models.job_type_statistics_filter import JobTypeStatisticsFilter


T = TypeVar("T", bound="JobTypeStatisticsQuery")


@_attrs_define
class JobTypeStatisticsQuery:
    """Job type statistics query.

    Attributes:
        filter_ (JobTypeStatisticsFilter | Unset): Job type statistics search filter.
        page (CursorBasedForwardPagination | Unset):
    """

    filter_: JobTypeStatisticsFilter | Unset = UNSET
    page: CursorBasedForwardPagination | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        page: dict[str, Any] | Unset = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cursor_based_forward_pagination import (
            CursorBasedForwardPagination,
        )
        from ..models.job_type_statistics_filter import JobTypeStatisticsFilter

        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: JobTypeStatisticsFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = JobTypeStatisticsFilter.from_dict(_filter_)

        _page = d.pop("page", UNSET)
        page: CursorBasedForwardPagination | Unset
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = CursorBasedForwardPagination.from_dict(_page)

        job_type_statistics_query = cls(
            filter_=filter_,
            page=page,
        )

        job_type_statistics_query.additional_properties = d
        return job_type_statistics_query

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
