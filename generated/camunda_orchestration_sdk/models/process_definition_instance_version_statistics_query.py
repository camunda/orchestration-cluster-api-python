from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.process_definition_instance_version_statistics_query_filter import (
        ProcessDefinitionInstanceVersionStatisticsQueryFilter,
    )
    from ..models.process_definition_instance_version_statistics_query_page import (
        ProcessDefinitionInstanceVersionStatisticsQueryPage,
    )
    from ..models.process_definition_instance_version_statistics_query_sort_request import (
        ProcessDefinitionInstanceVersionStatisticsQuerySortRequest,
    )


T = TypeVar("T", bound="ProcessDefinitionInstanceVersionStatisticsQuery")


@_attrs_define
class ProcessDefinitionInstanceVersionStatisticsQuery:
    """
    Attributes:
        filter_ (ProcessDefinitionInstanceVersionStatisticsQueryFilter): The process definition instance version
            statistics search filters.
        page (ProcessDefinitionInstanceVersionStatisticsQueryPage | Unset): Pagination criteria.
        sort (list[ProcessDefinitionInstanceVersionStatisticsQuerySortRequest] | Unset): Sort field criteria.
    """

    filter_: ProcessDefinitionInstanceVersionStatisticsQueryFilter
    page: ProcessDefinitionInstanceVersionStatisticsQueryPage | Unset = UNSET
    sort: list[ProcessDefinitionInstanceVersionStatisticsQuerySortRequest] | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        page: dict[str, Any] | Unset = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        sort: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()
                sort.append(sort_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filter": filter_,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_definition_instance_version_statistics_query_filter import (
            ProcessDefinitionInstanceVersionStatisticsQueryFilter,
        )
        from ..models.process_definition_instance_version_statistics_query_page import (
            ProcessDefinitionInstanceVersionStatisticsQueryPage,
        )
        from ..models.process_definition_instance_version_statistics_query_sort_request import (
            ProcessDefinitionInstanceVersionStatisticsQuerySortRequest,
        )

        d = dict(src_dict)
        filter_ = ProcessDefinitionInstanceVersionStatisticsQueryFilter.from_dict(
            d.pop("filter")
        )

        _page = d.pop("page", UNSET)
        page: ProcessDefinitionInstanceVersionStatisticsQueryPage | Unset
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = ProcessDefinitionInstanceVersionStatisticsQueryPage.from_dict(_page)

        _sort = d.pop("sort", UNSET)
        sort: (
            list[ProcessDefinitionInstanceVersionStatisticsQuerySortRequest] | Unset
        ) = UNSET
        if _sort is not UNSET:
            sort = []
            for sort_item_data in _sort:
                sort_item = ProcessDefinitionInstanceVersionStatisticsQuerySortRequest.from_dict(
                    sort_item_data
                )

                sort.append(sort_item)

        process_definition_instance_version_statistics_query = cls(
            filter_=filter_,
            page=page,
            sort=sort,
        )

        process_definition_instance_version_statistics_query.additional_properties = d
        return process_definition_instance_version_statistics_query

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
