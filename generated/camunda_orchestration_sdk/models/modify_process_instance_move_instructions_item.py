from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId, lift_element_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.direct_ancestor_key_instruction import DirectAncestorKeyInstruction
    from ..models.inferred_ancestor_key_instruction import (
        InferredAncestorKeyInstruction,
    )
    from ..models.modify_process_instance_variable_instruction import (
        ModifyProcessInstanceVariableInstruction,
    )
    from ..models.source_element_instance_key_instruction import (
        SourceElementInstanceKeyInstruction,
    )
    from ..models.source_element_instruction_object import (
        SourceElementInstructionObject,
    )
    from ..models.use_source_parent_key_instruction import UseSourceParentKeyInstruction


T = TypeVar("T", bound="ModifyProcessInstanceMoveInstructionsItem")


@_attrs_define
class ModifyProcessInstanceMoveInstructionsItem:
    """Instruction describing a move operation. This instruction will terminate active element
    instances based on the sourceElementInstruction and activate a new element instance for each terminated
    one at targetElementId. Note that, for multi-instance activities, only the multi-instance
    body instances will activate new element instances at the target id.

        Attributes:
            source_element_instruction (SourceElementInstanceKeyInstruction | SourceElementInstructionObject): Defines the
                source element identifier for the move instruction. It can either be a sourceElementId, or
                sourceElementInstanceKey.
            target_element_id (str): The target element id. Example: Activity_106kosb.
            ancestor_scope_instruction (DirectAncestorKeyInstruction | InferredAncestorKeyInstruction | Unset |
                UseSourceParentKeyInstruction): Defines the ancestor scope for the created element instances. The default
                behavior resembles
                a "direct" scope instruction with an `ancestorElementInstanceKey` of `"-1"`.
            variable_instructions (list[ModifyProcessInstanceVariableInstruction] | Unset): Instructions describing which
                variables to create or update.
    """

    source_element_instruction: (
        SourceElementInstanceKeyInstruction | SourceElementInstructionObject
    )
    target_element_id: ElementId
    ancestor_scope_instruction: (
        DirectAncestorKeyInstruction
        | InferredAncestorKeyInstruction
        | Unset
        | UseSourceParentKeyInstruction
    ) = UNSET
    variable_instructions: list[ModifyProcessInstanceVariableInstruction] | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.direct_ancestor_key_instruction import (
            DirectAncestorKeyInstruction,
        )
        from ..models.inferred_ancestor_key_instruction import (
            InferredAncestorKeyInstruction,
        )
        from ..models.source_element_instruction_object import (
            SourceElementInstructionObject,
        )

        source_element_instruction: dict[str, Any]
        if isinstance(self.source_element_instruction, SourceElementInstructionObject):
            source_element_instruction = self.source_element_instruction.to_dict()
        else:
            source_element_instruction = self.source_element_instruction.to_dict()

        target_element_id = self.target_element_id

        ancestor_scope_instruction: dict[str, Any] | Unset
        if isinstance(self.ancestor_scope_instruction, Unset):
            ancestor_scope_instruction = UNSET
        elif isinstance(self.ancestor_scope_instruction, DirectAncestorKeyInstruction):
            ancestor_scope_instruction = self.ancestor_scope_instruction.to_dict()
        elif isinstance(
            self.ancestor_scope_instruction, InferredAncestorKeyInstruction
        ):
            ancestor_scope_instruction = self.ancestor_scope_instruction.to_dict()
        else:
            ancestor_scope_instruction = self.ancestor_scope_instruction.to_dict()

        variable_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variable_instructions, Unset):
            variable_instructions = []
            for variable_instructions_item_data in self.variable_instructions:
                variable_instructions_item = variable_instructions_item_data.to_dict()
                variable_instructions.append(variable_instructions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sourceElementInstruction": source_element_instruction,
                "targetElementId": target_element_id,
            }
        )
        if ancestor_scope_instruction is not UNSET:
            field_dict["ancestorScopeInstruction"] = ancestor_scope_instruction
        if variable_instructions is not UNSET:
            field_dict["variableInstructions"] = variable_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.direct_ancestor_key_instruction import (
            DirectAncestorKeyInstruction,
        )
        from ..models.inferred_ancestor_key_instruction import (
            InferredAncestorKeyInstruction,
        )
        from ..models.modify_process_instance_variable_instruction import (
            ModifyProcessInstanceVariableInstruction,
        )
        from ..models.source_element_instance_key_instruction import (
            SourceElementInstanceKeyInstruction,
        )
        from ..models.source_element_instruction_object import (
            SourceElementInstructionObject,
        )
        from ..models.use_source_parent_key_instruction import (
            UseSourceParentKeyInstruction,
        )

        d = dict(src_dict)

        def _parse_source_element_instruction(
            data: object,
        ) -> SourceElementInstanceKeyInstruction | SourceElementInstructionObject:
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                source_element_instruction_type_0 = (
                    SourceElementInstructionObject.from_dict(data)
                )

                return source_element_instruction_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            source_element_instruction_type_1 = (
                SourceElementInstanceKeyInstruction.from_dict(data)
            )

            return source_element_instruction_type_1

        source_element_instruction = _parse_source_element_instruction(
            d.pop("sourceElementInstruction")
        )

        target_element_id = lift_element_id(d.pop("targetElementId"))

        def _parse_ancestor_scope_instruction(
            data: object,
        ) -> (
            DirectAncestorKeyInstruction
            | InferredAncestorKeyInstruction
            | Unset
            | UseSourceParentKeyInstruction
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_ancestor_scope_instruction_type_0 = (
                    DirectAncestorKeyInstruction.from_dict(data)
                )

                return componentsschemas_ancestor_scope_instruction_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_ancestor_scope_instruction_type_1 = (
                    InferredAncestorKeyInstruction.from_dict(data)
                )

                return componentsschemas_ancestor_scope_instruction_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            componentsschemas_ancestor_scope_instruction_type_2 = (
                UseSourceParentKeyInstruction.from_dict(data)
            )

            return componentsschemas_ancestor_scope_instruction_type_2

        ancestor_scope_instruction = _parse_ancestor_scope_instruction(
            d.pop("ancestorScopeInstruction", UNSET)
        )

        _variable_instructions = d.pop("variableInstructions", UNSET)
        variable_instructions: (
            list[ModifyProcessInstanceVariableInstruction] | Unset
        ) = UNSET
        if _variable_instructions is not UNSET:
            variable_instructions = []
            for variable_instructions_item_data in _variable_instructions:
                variable_instructions_item = (
                    ModifyProcessInstanceVariableInstruction.from_dict(
                        variable_instructions_item_data
                    )
                )

                variable_instructions.append(variable_instructions_item)

        modify_process_instance_move_instructions_item = cls(
            source_element_instruction=source_element_instruction,
            target_element_id=target_element_id,
            ancestor_scope_instruction=ancestor_scope_instruction,
            variable_instructions=variable_instructions,
        )

        modify_process_instance_move_instructions_item.additional_properties = d
        return modify_process_instance_move_instructions_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
