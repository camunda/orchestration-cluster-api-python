from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationInstanceKey,
    TenantId,
)
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.evaluated_decision_input_item import EvaluatedDecisionInputItem
from ..models.matched_decision_rule_item import MatchedDecisionRuleItem

T = TypeVar("T", bound="EvaluatedDecisionResult")

@_attrs_define
class EvaluatedDecisionResult:
    decision_definition_id: DecisionDefinitionId | Unset = UNSET
    decision_definition_name: str | Unset = UNSET
    decision_definition_version: int | Unset = UNSET
    decision_definition_type: str | Unset = UNSET
    output: str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    matched_rules: list[MatchedDecisionRuleItem] | Unset = UNSET
    evaluated_inputs: list[EvaluatedDecisionInputItem] | Unset = UNSET
    decision_definition_key: DecisionDefinitionKey | Unset = UNSET
    decision_evaluation_instance_key: DecisionEvaluationInstanceKey | Unset = UNSET
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
