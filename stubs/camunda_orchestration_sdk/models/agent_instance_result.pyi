from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import AgentInstanceKey, ElementId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
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
T = TypeVar("T", bound="AgentInstanceResult")
@_attrs_define
class AgentInstanceResult:
    agent_instance_key: AgentInstanceKey
    status: AgentInstanceStatusEnum
    definition: AgentInstanceResultDefinition
    metrics: AgentInstanceResultMetrics
    limits: AgentInstanceResultLimits
    element_id: ElementId
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    tenant_id: TenantId
    creation_date: datetime.datetime
    last_updated_date: datetime.datetime
    completion_date: datetime.datetime | None
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
