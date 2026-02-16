from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.audit_log_actor_type_exact_match import AuditLogActorTypeExactMatch
from ..models.audit_log_result_exact_match import AuditLogResultExactMatch
from ..models.operation_type_exact_match import OperationTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
from ..models.advanced_result_filter import AdvancedResultFilter
from ..models.advanced_string_filter import AdvancedStringFilter

T = TypeVar("T", bound="UserTaskAuditLogFilter")

@_attrs_define
class UserTaskAuditLogFilter:
    operation_type: AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset = (
        UNSET
    )
    result: AdvancedResultFilter | AuditLogResultExactMatch | Unset = UNSET
    timestamp: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    actor_type: AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset = UNSET
    actor_id: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
