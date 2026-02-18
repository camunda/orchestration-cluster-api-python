from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, DecisionDefinitionKey, DecisionEvaluationInstanceKey, DecisionEvaluationKey, ElementInstanceKey, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.decision_definition_type_enum import DecisionDefinitionTypeEnum
from ..models.decision_instance_state_enum import DecisionInstanceStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.evaluated_decision_input_item import EvaluatedDecisionInputItem
from ..models.matched_decision_rule_item import MatchedDecisionRuleItem
T = TypeVar("T", bound="DecisionInstanceGetQueryResult")
@_attrs_define
class DecisionInstanceGetQueryResult:
    decision_evaluation_instance_key: DecisionEvaluationInstanceKey | Unset = UNSET
    state: DecisionInstanceStateEnum | Unset = UNSET
    evaluation_date: datetime.datetime | Unset = UNSET
    evaluation_failure: str | Unset = UNSET
    decision_definition_id: DecisionDefinitionId | Unset = UNSET
    decision_definition_name: str | Unset = UNSET
    decision_definition_version: int | Unset = UNSET
    decision_definition_type: DecisionDefinitionTypeEnum | Unset = UNSET
    result: str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    decision_evaluation_key: DecisionEvaluationKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    root_process_instance_key: str | Unset = UNSET
    decision_definition_key: DecisionDefinitionKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    root_decision_definition_key: DecisionDefinitionKey | Unset = UNSET
    evaluated_inputs: list[EvaluatedDecisionInputItem] | Unset = UNSET
    matched_rules: list[MatchedDecisionRuleItem] | Unset = UNSET
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
