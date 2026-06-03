from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.process_definition_instance_version_statistics_query_filter import ProcessDefinitionInstanceVersionStatisticsQueryFilter
from ..models.process_definition_instance_version_statistics_query_page import ProcessDefinitionInstanceVersionStatisticsQueryPage
from ..models.process_definition_instance_version_statistics_query_sort_request import ProcessDefinitionInstanceVersionStatisticsQuerySortRequest
T = TypeVar("T", bound="ProcessDefinitionInstanceVersionStatisticsQuery")
@_attrs_define
class ProcessDefinitionInstanceVersionStatisticsQuery:
    filter_: ProcessDefinitionInstanceVersionStatisticsQueryFilter
    page: ProcessDefinitionInstanceVersionStatisticsQueryPage | Unset = UNSET
    sort: list[ProcessDefinitionInstanceVersionStatisticsQuerySortRequest] | Unset = (
            UNSET
        )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
