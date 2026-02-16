from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.decision_evaluation_by_id_variables import DecisionEvaluationByIdVariables

T = TypeVar("T", bound="DecisionEvaluationByID")

@_attrs_define
class DecisionEvaluationByID:
    decision_definition_id: DecisionDefinitionId
    variables: DecisionEvaluationByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
