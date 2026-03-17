from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, DecisionDefinitionKey, DecisionEvaluationInstanceKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.evaluated_decision_input_item import EvaluatedDecisionInputItem
from ..models.matched_decision_rule_item import MatchedDecisionRuleItem
T = TypeVar("T", bound="EvaluatedDecisionResult")
@_attrs_define
class EvaluatedDecisionResult:
    decision_definition_id: DecisionDefinitionId
    decision_definition_name: str
    decision_definition_version: int
    decision_definition_type: str
    output: str
    tenant_id: TenantId
    matched_rules: list[MatchedDecisionRuleItem]
    evaluated_inputs: list[EvaluatedDecisionInputItem]
    decision_definition_key: DecisionDefinitionKey
    decision_evaluation_instance_key: DecisionEvaluationInstanceKey
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
