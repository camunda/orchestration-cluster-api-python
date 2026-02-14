from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.incident_process_instance_statistics_by_definition_query_filter import (
        IncidentProcessInstanceStatisticsByDefinitionQueryFilter,
    )
    from ..models.incident_process_instance_statistics_by_definition_query_page import (
        IncidentProcessInstanceStatisticsByDefinitionQueryPage,
    )
    from ..models.incident_process_instance_statistics_by_definition_query_sort_request import (
        IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest,
    )


T = TypeVar("T", bound="IncidentProcessInstanceStatisticsByDefinitionQuery")


@_attrs_define
class IncidentProcessInstanceStatisticsByDefinitionQuery:
    """
    Attributes:
        filter_ (IncidentProcessInstanceStatisticsByDefinitionQueryFilter): Filter criteria for the aggregated process
            instance statistics.
        page (IncidentProcessInstanceStatisticsByDefinitionQueryPage | Unset): Pagination parameters for the aggregated
            process instance statistics.
        sort (list[IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest] | Unset): Sorting criteria for process
            instance statistics grouped by process definition.
    """

    filter_: IncidentProcessInstanceStatisticsByDefinitionQueryFilter
    page: IncidentProcessInstanceStatisticsByDefinitionQueryPage | Unset = UNSET
    sort: (
        list[IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest] | Unset
    ) = UNSET
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
        from ..models.incident_process_instance_statistics_by_definition_query_filter import (
            IncidentProcessInstanceStatisticsByDefinitionQueryFilter,
        )
        from ..models.incident_process_instance_statistics_by_definition_query_page import (
            IncidentProcessInstanceStatisticsByDefinitionQueryPage,
        )
        from ..models.incident_process_instance_statistics_by_definition_query_sort_request import (
            IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest,
        )

        d = dict(src_dict)
        filter_ = IncidentProcessInstanceStatisticsByDefinitionQueryFilter.from_dict(
            d.pop("filter")
        )

        _page = d.pop("page", UNSET)
        page: IncidentProcessInstanceStatisticsByDefinitionQueryPage | Unset
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = IncidentProcessInstanceStatisticsByDefinitionQueryPage.from_dict(
                _page
            )

        _sort = d.pop("sort", UNSET)
        sort: (
            list[IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest] | Unset
        ) = UNSET
        if _sort is not UNSET:
            sort = []
            for sort_item_data in _sort:
                sort_item = IncidentProcessInstanceStatisticsByDefinitionQuerySortRequest.from_dict(
                    sort_item_data
                )

                sort.append(sort_item)

        incident_process_instance_statistics_by_definition_query = cls(
            filter_=filter_,
            page=page,
            sort=sort,
        )

        incident_process_instance_statistics_by_definition_query.additional_properties = d
        return incident_process_instance_statistics_by_definition_query

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
