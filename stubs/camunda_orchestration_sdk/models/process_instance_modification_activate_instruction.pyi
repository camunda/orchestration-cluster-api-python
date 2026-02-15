from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.modify_process_instance_variable_instruction import ModifyProcessInstanceVariableInstruction
T = TypeVar("T", bound="ProcessInstanceModificationActivateInstruction")
@_attrs_define
class ProcessInstanceModificationActivateInstruction:
    element_id: ElementId
    variable_instructions: list[ModifyProcessInstanceVariableInstruction] | Unset = (
            UNSET
        )
    ancestor_element_instance_key: str | Unset = UNSET
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
