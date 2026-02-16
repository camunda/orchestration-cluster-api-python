from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.modify_process_instance_move_instructions_item import (
    ModifyProcessInstanceMoveInstructionsItem,
)
from ..models.process_instance_modification_activate_instruction import (
    ProcessInstanceModificationActivateInstruction,
)
from ..models.process_instance_modification_terminate_by_key_instruction import (
    ProcessInstanceModificationTerminateByKeyInstruction,
)
from ..models.terminate_instructions_item_object import TerminateInstructionsItemObject

T = TypeVar("T", bound="ModifyProcessInstanceData")

@_attrs_define
class ModifyProcessInstanceData:
    operation_reference: int | Unset = UNSET
    activate_instructions: (
        list[ProcessInstanceModificationActivateInstruction] | Unset
    ) = UNSET
    move_instructions: list[ModifyProcessInstanceMoveInstructionsItem] | Unset = UNSET
    terminate_instructions: (
        list[
            ProcessInstanceModificationTerminateByKeyInstruction
            | TerminateInstructionsItemObject
        ]
        | Unset
    ) = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
