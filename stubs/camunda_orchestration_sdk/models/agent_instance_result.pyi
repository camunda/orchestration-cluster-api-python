from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    AgentInstanceKey,
    ElementId,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.agent_instance_status_enum import AgentInstanceStatusEnum
from ..models.agent_instance_result_definition import AgentInstanceResultDefinition
from ..models.agent_instance_result_limits import AgentInstanceResultLimits
from ..models.agent_instance_result_metrics import AgentInstanceResultMetrics
from ..models.agent_tool import AgentTool

T = TypeVar("T", bound="AgentInstanceResult")

@_attrs_define
class AgentInstanceResult:
    agent_instance_key: AgentInstanceKey
    status: AgentInstanceStatusEnum
    definition: AgentInstanceResultDefinition
    metrics: AgentInstanceResultMetrics
    limits: AgentInstanceResultLimits
    tools: list[AgentTool]
    element_id: ElementId
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    process_definition_id: ProcessDefinitionId
    process_definition_version: int
    process_definition_version_tag: None | str
    tenant_id: TenantId
    creation_date: datetime.datetime
    last_updated_date: datetime.datetime
    completion_date: datetime.datetime | None
    element_instance_keys: list[str]
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
