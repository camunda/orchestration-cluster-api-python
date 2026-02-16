from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.incident_process_instance_statistics_by_error_query_page import (
    IncidentProcessInstanceStatisticsByErrorQueryPage,
)
from ..models.incident_process_instance_statistics_by_error_query_sort_request import (
    IncidentProcessInstanceStatisticsByErrorQuerySortRequest,
)

T = TypeVar("T", bound="IncidentProcessInstanceStatisticsByErrorQuery")

@_attrs_define
class IncidentProcessInstanceStatisticsByErrorQuery:
    page: IncidentProcessInstanceStatisticsByErrorQueryPage | Unset = UNSET
    sort: list[IncidentProcessInstanceStatisticsByErrorQuerySortRequest] | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
