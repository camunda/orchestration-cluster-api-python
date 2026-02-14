from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modify_process_instance_move_instructions_item import (
        ModifyProcessInstanceMoveInstructionsItem,
    )
    from ..models.process_instance_modification_activate_instruction import (
        ProcessInstanceModificationActivateInstruction,
    )
    from ..models.process_instance_modification_terminate_by_key_instruction import (
        ProcessInstanceModificationTerminateByKeyInstruction,
    )
    from ..models.terminate_instructions_item_object import (
        TerminateInstructionsItemObject,
    )


T = TypeVar("T", bound="ModifyProcessInstanceData")


@_attrs_define
class ModifyProcessInstanceData:
    """
    Attributes:
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
        activate_instructions (list[ProcessInstanceModificationActivateInstruction] | Unset): Instructions describing
            which elements to activate in which scopes and which variables to create or update.
        move_instructions (list[ModifyProcessInstanceMoveInstructionsItem] | Unset): Instructions describing which
            elements to move from one scope to another.
        terminate_instructions (list[ProcessInstanceModificationTerminateByKeyInstruction |
            TerminateInstructionsItemObject] | Unset): Instructions describing which elements to terminate.
    """

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

    def to_dict(self) -> dict[str, Any]:
        from ..models.terminate_instructions_item_object import (
            TerminateInstructionsItemObject,
        )

        operation_reference = self.operation_reference

        activate_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.activate_instructions, Unset):
            activate_instructions = []
            for activate_instructions_item_data in self.activate_instructions:
                activate_instructions_item = activate_instructions_item_data.to_dict()
                activate_instructions.append(activate_instructions_item)

        move_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.move_instructions, Unset):
            move_instructions = []
            for move_instructions_item_data in self.move_instructions:
                move_instructions_item = move_instructions_item_data.to_dict()
                move_instructions.append(move_instructions_item)

        terminate_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.terminate_instructions, Unset):
            terminate_instructions = []
            for terminate_instructions_item_data in self.terminate_instructions:
                terminate_instructions_item: dict[str, Any]
                if isinstance(
                    terminate_instructions_item_data, TerminateInstructionsItemObject
                ):
                    terminate_instructions_item = (
                        terminate_instructions_item_data.to_dict()
                    )
                else:
                    terminate_instructions_item = (
                        terminate_instructions_item_data.to_dict()
                    )

                terminate_instructions.append(terminate_instructions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference
        if activate_instructions is not UNSET:
            field_dict["activateInstructions"] = activate_instructions
        if move_instructions is not UNSET:
            field_dict["moveInstructions"] = move_instructions
        if terminate_instructions is not UNSET:
            field_dict["terminateInstructions"] = terminate_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.modify_process_instance_move_instructions_item import (
            ModifyProcessInstanceMoveInstructionsItem,
        )
        from ..models.process_instance_modification_activate_instruction import (
            ProcessInstanceModificationActivateInstruction,
        )
        from ..models.process_instance_modification_terminate_by_key_instruction import (
            ProcessInstanceModificationTerminateByKeyInstruction,
        )
        from ..models.terminate_instructions_item_object import (
            TerminateInstructionsItemObject,
        )

        d = dict(src_dict)
        operation_reference = d.pop("operationReference", UNSET)

        _activate_instructions = d.pop("activateInstructions", UNSET)
        activate_instructions: (
            list[ProcessInstanceModificationActivateInstruction] | Unset
        ) = UNSET
        if _activate_instructions is not UNSET:
            activate_instructions = []
            for activate_instructions_item_data in _activate_instructions:
                activate_instructions_item = (
                    ProcessInstanceModificationActivateInstruction.from_dict(
                        activate_instructions_item_data
                    )
                )

                activate_instructions.append(activate_instructions_item)

        _move_instructions = d.pop("moveInstructions", UNSET)
        move_instructions: list[ModifyProcessInstanceMoveInstructionsItem] | Unset = (
            UNSET
        )
        if _move_instructions is not UNSET:
            move_instructions = []
            for move_instructions_item_data in _move_instructions:
                move_instructions_item = (
                    ModifyProcessInstanceMoveInstructionsItem.from_dict(
                        move_instructions_item_data
                    )
                )

                move_instructions.append(move_instructions_item)

        _terminate_instructions = d.pop("terminateInstructions", UNSET)
        terminate_instructions: (
            list[
                ProcessInstanceModificationTerminateByKeyInstruction
                | TerminateInstructionsItemObject
            ]
            | Unset
        ) = UNSET
        if _terminate_instructions is not UNSET:
            terminate_instructions = []
            for terminate_instructions_item_data in _terminate_instructions:

                def _parse_terminate_instructions_item(
                    data: object,
                ) -> (
                    ProcessInstanceModificationTerminateByKeyInstruction
                    | TerminateInstructionsItemObject
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()

                        data = cast(dict[str, Any], data)
                        terminate_instructions_item_type_0 = (
                            TerminateInstructionsItemObject.from_dict(data)
                        )

                        return terminate_instructions_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    terminate_instructions_item_type_1 = (
                        ProcessInstanceModificationTerminateByKeyInstruction.from_dict(
                            data
                        )
                    )

                    return terminate_instructions_item_type_1

                terminate_instructions_item = _parse_terminate_instructions_item(
                    terminate_instructions_item_data
                )

                terminate_instructions.append(terminate_instructions_item)

        modify_process_instance_data = cls(
            operation_reference=operation_reference,
            activate_instructions=activate_instructions,
            move_instructions=move_instructions,
            terminate_instructions=terminate_instructions,
        )

        return modify_process_instance_data
