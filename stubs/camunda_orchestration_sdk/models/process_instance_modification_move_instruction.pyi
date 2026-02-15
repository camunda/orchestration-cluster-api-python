from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.direct_ancestor_key_instruction import DirectAncestorKeyInstruction
from ..models.inferred_ancestor_key_instruction import InferredAncestorKeyInstruction
from ..models.modify_process_instance_variable_instruction import ModifyProcessInstanceVariableInstruction
from ..models.source_element_id_instruction import SourceElementIdInstruction
from ..models.source_element_instance_key_instruction import SourceElementInstanceKeyInstruction
from ..models.use_source_parent_key_instruction import UseSourceParentKeyInstruction
T = TypeVar("T", bound="ProcessInstanceModificationMoveInstruction")
@_attrs_define
class ProcessInstanceModificationMoveInstruction:
    source_element_instruction: (
            SourceElementIdInstruction | SourceElementInstanceKeyInstruction
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
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
