from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.process_instance_modification_activate_instruction import ProcessInstanceModificationActivateInstruction
from ..models.process_instance_modification_move_instruction import ProcessInstanceModificationMoveInstruction
from ..models.process_instance_modification_terminate_by_id_instruction import ProcessInstanceModificationTerminateByIdInstruction
from ..models.process_instance_modification_terminate_by_key_instruction import ProcessInstanceModificationTerminateByKeyInstruction
T = TypeVar("T", bound="ProcessInstanceModificationInstruction")
@_attrs_define
class ProcessInstanceModificationInstruction:
    operation_reference: int | Unset = UNSET
    activate_instructions: (
            list[ProcessInstanceModificationActivateInstruction] | Unset
        ) = UNSET
    move_instructions: list[ProcessInstanceModificationMoveInstruction] | Unset = UNSET
    terminate_instructions: (
            list[
                ProcessInstanceModificationTerminateByIdInstruction
                | ProcessInstanceModificationTerminateByKeyInstruction
            ]
            | Unset
        ) = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
