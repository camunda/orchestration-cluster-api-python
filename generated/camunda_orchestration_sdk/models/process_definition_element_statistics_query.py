from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_definition_element_statistics_query_filter import (
        ProcessDefinitionElementStatisticsQueryFilter,
    )


T = TypeVar("T", bound="ProcessDefinitionElementStatisticsQuery")


@_attrs_define
class ProcessDefinitionElementStatisticsQuery:
    """Process definition element statistics request.

    Attributes:
        filter_ (ProcessDefinitionElementStatisticsQueryFilter | Unset): The process definition statistics search
            filters.
    """

    filter_: ProcessDefinitionElementStatisticsQueryFilter | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_definition_element_statistics_query_filter import (
            ProcessDefinitionElementStatisticsQueryFilter,
        )

        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: ProcessDefinitionElementStatisticsQueryFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = ProcessDefinitionElementStatisticsQueryFilter.from_dict(_filter_)

        process_definition_element_statistics_query = cls(
            filter_=filter_,
        )

        return process_definition_element_statistics_query
