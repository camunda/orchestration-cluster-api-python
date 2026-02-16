from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.process_instance_cancellation_batch_operation_request_filter import ProcessInstanceCancellationBatchOperationRequestFilter
from ..models.process_instance_modification_move_batch_operation_instruction import ProcessInstanceModificationMoveBatchOperationInstruction
T = TypeVar("T", bound="ModifyProcessInstancesBatchOperationData")
@_attrs_define
class ModifyProcessInstancesBatchOperationData:
    filter_: ProcessInstanceCancellationBatchOperationRequestFilter
    move_instructions: list[ProcessInstanceModificationMoveBatchOperationInstruction]
    operation_reference: int | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
