from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_instance_cancellation_batch_operation_request_filter import (
        ProcessInstanceCancellationBatchOperationRequestFilter,
    )
    from ..models.process_instance_modification_move_batch_operation_instruction import (
        ProcessInstanceModificationMoveBatchOperationInstruction,
    )


T = TypeVar("T", bound="ProcessInstanceModificationBatchOperationRequest")


@_attrs_define
class ProcessInstanceModificationBatchOperationRequest:
    """The process instance filter to define on which process instances tokens should be moved,
    and new element instances should be activated or terminated.

        Attributes:
            filter_ (ProcessInstanceCancellationBatchOperationRequestFilter): The process instance filter.
            move_instructions (list[ProcessInstanceModificationMoveBatchOperationInstruction]): Instructions for moving
                tokens between elements.
            operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
                from this operation.
                Must be > 0 if provided.
    """

    filter_: ProcessInstanceCancellationBatchOperationRequestFilter
    move_instructions: list[ProcessInstanceModificationMoveBatchOperationInstruction]
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        move_instructions: list[dict[str, Any]] = []
        for move_instructions_item_data in self.move_instructions:
            move_instructions_item = move_instructions_item_data.to_dict()
            move_instructions.append(move_instructions_item)

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "filter": filter_,
                "moveInstructions": move_instructions,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_instance_cancellation_batch_operation_request_filter import (
            ProcessInstanceCancellationBatchOperationRequestFilter,
        )
        from ..models.process_instance_modification_move_batch_operation_instruction import (
            ProcessInstanceModificationMoveBatchOperationInstruction,
        )

        d = dict(src_dict)
        filter_ = ProcessInstanceCancellationBatchOperationRequestFilter.from_dict(
            d.pop("filter")
        )

        move_instructions: list[
            ProcessInstanceModificationMoveBatchOperationInstruction
        ] = []
        _move_instructions = d.pop("moveInstructions")
        for move_instructions_item_data in _move_instructions:
            move_instructions_item = (
                ProcessInstanceModificationMoveBatchOperationInstruction.from_dict(
                    move_instructions_item_data
                )
            )

            move_instructions.append(move_instructions_item)

        operation_reference = d.pop("operationReference", UNSET)

        process_instance_modification_batch_operation_request = cls(
            filter_=filter_,
            move_instructions=move_instructions,
            operation_reference=operation_reference,
        )

        return process_instance_modification_batch_operation_request
