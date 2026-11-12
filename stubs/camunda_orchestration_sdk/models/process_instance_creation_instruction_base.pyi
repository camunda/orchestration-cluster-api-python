from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import BusinessId, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.process_instance_creation_instruction_base_variables import (
    ProcessInstanceCreationInstructionBaseVariables,
)
from ..models.process_instance_creation_start_instruction import (
    ProcessInstanceCreationStartInstruction,
)
from ..models.process_instance_creation_terminate_instruction import (
    ProcessInstanceCreationTerminateInstruction,
)

T = TypeVar("T", bound="ProcessInstanceCreationInstructionBase")

@_attrs_define
class ProcessInstanceCreationInstructionBase:
    variables: ProcessInstanceCreationInstructionBaseVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    operation_reference: int | Unset = UNSET
    start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = UNSET
    runtime_instructions: list[ProcessInstanceCreationTerminateInstruction] | Unset = (
        UNSET
    )
    await_completion: bool | Unset = UNSET
    fetch_variables: list[str] | Unset = UNSET
    request_timeout: int | Unset = UNSET
    tags: list[str] | Unset = UNSET
    business_id: BusinessId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
