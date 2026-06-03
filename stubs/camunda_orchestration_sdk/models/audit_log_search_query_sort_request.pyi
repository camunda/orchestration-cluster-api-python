from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.audit_log_search_query_sort_request_field import AuditLogSearchQuerySortRequestField
from ..models.sort_order_enum import SortOrderEnum
from ..types import UNSET, Unset
T = TypeVar("T", bound="AuditLogSearchQuerySortRequest")
@_attrs_define
class AuditLogSearchQuerySortRequest:
    field: AuditLogSearchQuerySortRequestField
    order: SortOrderEnum | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
