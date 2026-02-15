from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionId, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.process_instance_creation_instruction_by_id_variables import ProcessInstanceCreationInstructionByIdVariables
from ..models.process_instance_creation_start_instruction import ProcessInstanceCreationStartInstruction
from ..models.process_instance_creation_terminate_instruction import ProcessInstanceCreationTerminateInstruction
T = TypeVar("T", bound="ProcessInstanceCreationInstructionById")
@_attrs_define
class ProcessInstanceCreationInstructionById:
    process_definition_id: ProcessDefinitionId
    process_definition_version: int | Unset = -1
    variables: ProcessInstanceCreationInstructionByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    operation_reference: int | Unset = UNSET
    start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = UNSET
    runtime_instructions: list[ProcessInstanceCreationTerminateInstruction] | Unset = (
            UNSET
        )
    await_completion: bool | Unset = False
    fetch_variables: list[str] | Unset = UNSET
    request_timeout: int | Unset = 0
    tags: list[str] | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
