from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    AgentDefinitionKey,
    ElementId,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    TenantId,
)
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.agent_definition_type_enum import AgentDefinitionTypeEnum

T = TypeVar("T", bound="AgentDefinitionResult")

@_attrs_define
class AgentDefinitionResult:
    agent_definition_key: AgentDefinitionKey
    agent_type: AgentDefinitionTypeEnum
    name: str
    element_id: ElementId
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_definition_version: int
    process_definition_version_tag: None | str
    tenant_id: TenantId
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
