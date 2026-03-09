from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, DecisionDefinitionKey, DecisionEvaluationInstanceKey, DecisionEvaluationKey, ElementInstanceKey, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.decision_definition_type_enum import DecisionDefinitionTypeEnum
from ..models.decision_instance_state_enum import DecisionInstanceStateEnum
T = TypeVar("T", bound="DecisionInstanceResult")
@_attrs_define
class DecisionInstanceResult:
    decision_definition_id: DecisionDefinitionId
    decision_definition_key: DecisionDefinitionKey
    decision_definition_name: str
    decision_definition_type: DecisionDefinitionTypeEnum
    decision_definition_version: int
    decision_evaluation_instance_key: DecisionEvaluationInstanceKey
    decision_evaluation_key: DecisionEvaluationKey
    element_instance_key: None | ElementInstanceKey
    evaluation_date: datetime.datetime
    evaluation_failure: None | str
    process_definition_key: None | ProcessDefinitionKey
    process_instance_key: None | ProcessInstanceKey
    result: str
    root_decision_definition_key: DecisionDefinitionKey
    root_process_instance_key: None | ProcessInstanceKey
    state: DecisionInstanceStateEnum
    tenant_id: TenantId
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
