from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, DecisionEvaluationKey, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.decision_definition_type_enum import DecisionDefinitionTypeEnum
from ..models.decision_instance_state_exact_match import DecisionInstanceStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_decision_definition_key_filter import AdvancedDecisionDefinitionKeyFilter
from ..models.advanced_decision_evaluation_instance_key_filter import AdvancedDecisionEvaluationInstanceKeyFilter
from ..models.advanced_decision_instance_state_filter import AdvancedDecisionInstanceStateFilter
from ..models.advanced_element_instance_key_filter import AdvancedElementInstanceKeyFilter
T = TypeVar("T", bound="DecisionInstanceSearchQueryFilter")
@_attrs_define
class DecisionInstanceSearchQueryFilter:
    decision_evaluation_instance_key: (
            AdvancedDecisionEvaluationInstanceKeyFilter | str | Unset
        ) = UNSET
    state: (
            AdvancedDecisionInstanceStateFilter | DecisionInstanceStateExactMatch | Unset
        ) = UNSET
    evaluation_failure: str | Unset = UNSET
    evaluation_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    decision_definition_id: DecisionDefinitionId | Unset = UNSET
    decision_definition_name: str | Unset = UNSET
    decision_definition_version: int | Unset = UNSET
    decision_definition_type: DecisionDefinitionTypeEnum | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    decision_evaluation_key: DecisionEvaluationKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    decision_definition_key: AdvancedDecisionDefinitionKeyFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    root_decision_definition_key: AdvancedDecisionDefinitionKeyFilter | str | Unset = (
            UNSET
        )
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
