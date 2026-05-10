from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.sort_order_enum import SortOrderEnum
from ..models.tenant_group_search_query_sort_request_field import (
    TenantGroupSearchQuerySortRequestField,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantGroupSearchQuerySortRequest")

@_attrs_define
class TenantGroupSearchQuerySortRequest:
    field: TenantGroupSearchQuerySortRequestField
    order: SortOrderEnum | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
