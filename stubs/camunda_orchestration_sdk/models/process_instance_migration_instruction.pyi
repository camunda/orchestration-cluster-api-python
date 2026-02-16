from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.migrate_process_instance_mapping_instruction import (
    MigrateProcessInstanceMappingInstruction,
)

T = TypeVar("T", bound="ProcessInstanceMigrationInstruction")

@_attrs_define
class ProcessInstanceMigrationInstruction:
    target_process_definition_key: ProcessDefinitionKey
    mapping_instructions: list[MigrateProcessInstanceMappingInstruction]
    operation_reference: int | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
