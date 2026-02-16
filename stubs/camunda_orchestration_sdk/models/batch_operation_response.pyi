from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import BatchOperationKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.audit_log_actor_type_enum import AuditLogActorTypeEnum
from ..models.batch_operation_state_enum import BatchOperationStateEnum
from ..models.batch_operation_type_enum import BatchOperationTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.batch_operation_error import BatchOperationError

T = TypeVar("T", bound="BatchOperationResponse")

@_attrs_define
class BatchOperationResponse:
    batch_operation_key: BatchOperationKey | Unset = UNSET
    state: BatchOperationStateEnum | Unset = UNSET
    batch_operation_type: BatchOperationTypeEnum | Unset = UNSET
    start_date: datetime.datetime | Unset = UNSET
    end_date: datetime.datetime | Unset = UNSET
    actor_type: AuditLogActorTypeEnum | Unset = UNSET
    actor_id: str | Unset = UNSET
    operations_total_count: int | Unset = UNSET
    operations_failed_count: int | Unset = UNSET
    operations_completed_count: int | Unset = UNSET
    errors: list[BatchOperationError] | Unset = UNSET
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
