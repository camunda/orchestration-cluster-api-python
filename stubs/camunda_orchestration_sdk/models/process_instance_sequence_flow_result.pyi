from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementId, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="ProcessInstanceSequenceFlowResult")
@_attrs_define
class ProcessInstanceSequenceFlowResult:
    root_process_instance_key: None | ProcessInstanceKey
    sequence_flow_id: str | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
