from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationKey,
    DecisionInstanceKey,
    DecisionRequirementsKey,
    TenantId,
)
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.evaluated_decision_result import EvaluatedDecisionResult

T = TypeVar("T", bound="EvaluateDecisionResult")

@_attrs_define
class EvaluateDecisionResult:
    decision_definition_id: DecisionDefinitionId
    decision_definition_name: str
    decision_definition_version: int
    decision_requirements_id: str
    output: str
    failed_decision_definition_id: DecisionDefinitionId
    failure_message: str
    tenant_id: TenantId
    decision_definition_key: DecisionDefinitionKey
    decision_requirements_key: DecisionRequirementsKey
    decision_evaluation_key: DecisionEvaluationKey
    evaluated_decisions: list[EvaluatedDecisionResult]
    decision_instance_key: DecisionInstanceKey | Unset = UNSET
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
