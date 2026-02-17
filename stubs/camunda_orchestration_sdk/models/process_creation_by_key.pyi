from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.process_instance_creation_instruction_by_id_variables import ProcessInstanceCreationInstructionByIdVariables
from ..models.process_instance_creation_start_instruction import ProcessInstanceCreationStartInstruction
from ..models.process_instance_creation_terminate_instruction import ProcessInstanceCreationTerminateInstruction
T = TypeVar("T", bound="ProcessCreationByKey")
@_attrs_define
class ProcessCreationByKey:
    process_definition_key: ProcessDefinitionKey
    variables: ProcessInstanceCreationInstructionByIdVariables | Unset = UNSET
    start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = UNSET
    runtime_instructions: list[ProcessInstanceCreationTerminateInstruction] | Unset = (
            UNSET
        )
    tenant_id: TenantId | Unset = UNSET
    operation_reference: int | Unset = UNSET
    await_completion: bool | Unset = False
    request_timeout: int | Unset = 0
    fetch_variables: list[str] | Unset = UNSET
    tags: list[str] | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
