from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.process_definition_instance_statistics_result import ProcessDefinitionInstanceStatisticsResult
from ..models.search_query_page_response import SearchQueryPageResponse
T = TypeVar("T", bound="ProcessDefinitionInstanceStatisticsQueryResult")
@_attrs_define
class ProcessDefinitionInstanceStatisticsQueryResult:
    items: list[ProcessDefinitionInstanceStatisticsResult]
    page: SearchQueryPageResponse
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
