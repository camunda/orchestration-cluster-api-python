from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.decision_instance_deletion_batch_operation_request_filter import DecisionInstanceDeletionBatchOperationRequestFilter
T = TypeVar("T", bound="DecisionInstanceDeletionBatchOperationRequest")
@_attrs_define
class DecisionInstanceDeletionBatchOperationRequest:
    filter_: DecisionInstanceDeletionBatchOperationRequestFilter
    operation_reference: int | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
