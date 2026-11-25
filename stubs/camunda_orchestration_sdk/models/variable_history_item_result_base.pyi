from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    ScopeKey,
    TenantId,
    VariableHistoryItemKey,
    VariableKey,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.variable_history_item_actor_type_enum import (
    VariableHistoryItemActorTypeEnum,
)
from ..models.variable_history_item_operation_type_enum import (
    VariableHistoryItemOperationTypeEnum,
)
from ..models.variable_history_item_variable_operation_type_enum import (
    VariableHistoryItemVariableOperationTypeEnum,
)

T = TypeVar("T", bound="VariableHistoryItemResultBase")

@_attrs_define
class VariableHistoryItemResultBase:
    variable_history_item_key: VariableHistoryItemKey
    variable_key: VariableKey
    name: str
    scope_key: ScopeKey
    element_instance_key: None | ElementInstanceKey
    element_id: None | ElementId
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId
    timestamp: datetime.datetime
    operation_type: VariableHistoryItemOperationTypeEnum
    variable_operation_type: VariableHistoryItemVariableOperationTypeEnum
    actor_type: VariableHistoryItemActorTypeEnum
    actor_id: None | str
    agent_element_id: None | ElementId
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
