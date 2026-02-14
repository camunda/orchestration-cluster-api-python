from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionKey,
    lift_process_definition_key,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.migrate_process_instance_mapping_instruction import (
        MigrateProcessInstanceMappingInstruction,
    )


T = TypeVar("T", bound="ProcessInstanceMigrationInstruction")


@_attrs_define
class ProcessInstanceMigrationInstruction:
    """The migration instructions describe how to migrate a process instance from one process definition to another.

    Attributes:
        target_process_definition_key (str): The key of process definition to migrate the process instance to. Example:
            2251799813686749.
        mapping_instructions (list[MigrateProcessInstanceMappingInstruction]): Element mappings from the source process
            instance to the target process instance.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
    """

    target_process_definition_key: ProcessDefinitionKey
    mapping_instructions: list[MigrateProcessInstanceMappingInstruction]
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        target_process_definition_key = self.target_process_definition_key

        mapping_instructions: list[dict[str, Any]] = []
        for mapping_instructions_item_data in self.mapping_instructions:
            mapping_instructions_item = mapping_instructions_item_data.to_dict()
            mapping_instructions.append(mapping_instructions_item)

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "targetProcessDefinitionKey": target_process_definition_key,
                "mappingInstructions": mapping_instructions,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.migrate_process_instance_mapping_instruction import (
            MigrateProcessInstanceMappingInstruction,
        )

        d = dict(src_dict)
        target_process_definition_key = lift_process_definition_key(
            d.pop("targetProcessDefinitionKey")
        )

        mapping_instructions: list[MigrateProcessInstanceMappingInstruction] = []
        _mapping_instructions = d.pop("mappingInstructions")
        for mapping_instructions_item_data in _mapping_instructions:
            mapping_instructions_item = (
                MigrateProcessInstanceMappingInstruction.from_dict(
                    mapping_instructions_item_data
                )
            )

            mapping_instructions.append(mapping_instructions_item)

        operation_reference = d.pop("operationReference", UNSET)

        process_instance_migration_instruction = cls(
            target_process_definition_key=target_process_definition_key,
            mapping_instructions=mapping_instructions,
            operation_reference=operation_reference,
        )

        return process_instance_migration_instruction
