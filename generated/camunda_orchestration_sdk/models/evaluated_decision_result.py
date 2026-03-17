from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationInstanceKey,
    TenantId,
    lift_decision_definition_id,
    lift_decision_definition_key,
    lift_decision_evaluation_instance_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.evaluated_decision_input_item import EvaluatedDecisionInputItem
    from ..models.matched_decision_rule_item import MatchedDecisionRuleItem


T = TypeVar("T", bound="EvaluatedDecisionResult")


@_attrs_define
class EvaluatedDecisionResult:
    """A decision that was evaluated.

    Attributes:
        decision_definition_id (str): The ID of the decision which was evaluated. Example: new-hire-onboarding-workflow.
        decision_definition_name (str): The name of the decision which was evaluated.
        decision_definition_version (int): The version of the decision which was evaluated.
        decision_definition_type (str): The type of the decision which was evaluated.
        output (str): JSON document that will instantiate the result of the decision which was evaluated.
        tenant_id (str): The tenant ID of the evaluated decision. Example: customer-service.
        matched_rules (list[MatchedDecisionRuleItem]): The decision rules that matched within this decision evaluation.
        evaluated_inputs (list[EvaluatedDecisionInputItem]): The decision inputs that were evaluated within this
            decision evaluation.
        decision_definition_key (str): The unique key identifying the decision which was evaluate. Example:
            2251799813326547.
        decision_evaluation_instance_key (str): The unique key identifying this decision evaluation instance. Example:
            2251799813684367.
    """

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
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        decision_definition_name = self.decision_definition_name

        decision_definition_version = self.decision_definition_version

        decision_definition_type = self.decision_definition_type

        output = self.output

        tenant_id = self.tenant_id

        matched_rules: list[dict[str, Any]] = []
        for matched_rules_item_data in self.matched_rules:
            matched_rules_item = matched_rules_item_data.to_dict()
            matched_rules.append(matched_rules_item)

        evaluated_inputs: list[dict[str, Any]] = []
        for evaluated_inputs_item_data in self.evaluated_inputs:
            evaluated_inputs_item = evaluated_inputs_item_data.to_dict()
            evaluated_inputs.append(evaluated_inputs_item)

        decision_definition_key = self.decision_definition_key

        decision_evaluation_instance_key = self.decision_evaluation_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
                "decisionDefinitionName": decision_definition_name,
                "decisionDefinitionVersion": decision_definition_version,
                "decisionDefinitionType": decision_definition_type,
                "output": output,
                "tenantId": tenant_id,
                "matchedRules": matched_rules,
                "evaluatedInputs": evaluated_inputs,
                "decisionDefinitionKey": decision_definition_key,
                "decisionEvaluationInstanceKey": decision_evaluation_instance_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluated_decision_input_item import EvaluatedDecisionInputItem
        from ..models.matched_decision_rule_item import MatchedDecisionRuleItem

        d = dict(src_dict)
        decision_definition_id = lift_decision_definition_id(
            d.pop("decisionDefinitionId")
        )

        decision_definition_name = d.pop("decisionDefinitionName")

        decision_definition_version = d.pop("decisionDefinitionVersion")

        decision_definition_type = d.pop("decisionDefinitionType")

        output = d.pop("output")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        matched_rules: list[MatchedDecisionRuleItem] = []
        _matched_rules = d.pop("matchedRules")
        for matched_rules_item_data in _matched_rules:
            matched_rules_item = MatchedDecisionRuleItem.from_dict(
                matched_rules_item_data
            )

            matched_rules.append(matched_rules_item)

        evaluated_inputs: list[EvaluatedDecisionInputItem] = []
        _evaluated_inputs = d.pop("evaluatedInputs")
        for evaluated_inputs_item_data in _evaluated_inputs:
            evaluated_inputs_item = EvaluatedDecisionInputItem.from_dict(
                evaluated_inputs_item_data
            )

            evaluated_inputs.append(evaluated_inputs_item)

        decision_definition_key = lift_decision_definition_key(
            d.pop("decisionDefinitionKey")
        )

        decision_evaluation_instance_key = lift_decision_evaluation_instance_key(
            d.pop("decisionEvaluationInstanceKey")
        )

        evaluated_decision_result = cls(
            decision_definition_id=decision_definition_id,
            decision_definition_name=decision_definition_name,
            decision_definition_version=decision_definition_version,
            decision_definition_type=decision_definition_type,
            output=output,
            tenant_id=tenant_id,
            matched_rules=matched_rules,
            evaluated_inputs=evaluated_inputs,
            decision_definition_key=decision_definition_key,
            decision_evaluation_instance_key=decision_evaluation_instance_key,
        )

        evaluated_decision_result.additional_properties = d
        return evaluated_decision_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
