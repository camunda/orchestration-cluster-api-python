from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.process_definition_element_statistics_query_filter import (
    ProcessDefinitionElementStatisticsQueryFilter,
)

T = TypeVar("T", bound="ProcessDefinitionElementStatisticsQuery")

@_attrs_define
class ProcessDefinitionElementStatisticsQuery:
    filter_: ProcessDefinitionElementStatisticsQueryFilter | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
