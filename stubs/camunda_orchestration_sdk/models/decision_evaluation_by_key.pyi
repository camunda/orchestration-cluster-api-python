from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.decision_evaluation_by_id_variables import DecisionEvaluationByIdVariables
T = TypeVar("T", bound="DecisionEvaluationByKey")
@_attrs_define
class DecisionEvaluationByKey:
    decision_definition_key: DecisionDefinitionKey
    variables: DecisionEvaluationByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
