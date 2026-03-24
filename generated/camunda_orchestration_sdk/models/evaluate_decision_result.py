from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationKey,
    DecisionInstanceKey,
    DecisionRequirementsKey,
    TenantId,
    lift_decision_definition_id,
    lift_decision_definition_key,
    lift_decision_evaluation_key,
    lift_decision_instance_key,
    lift_decision_requirements_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.evaluated_decision_result import EvaluatedDecisionResult


T = TypeVar("T", bound="EvaluateDecisionResult")


@_attrs_define
class EvaluateDecisionResult:
    """
    Attributes:
        decision_definition_id (str): The ID of the decision which was evaluated. Example: new-hire-onboarding-workflow.
        decision_definition_key (str): The unique key identifying the decision which was evaluated. Example:
            2251799813326547.
        decision_definition_name (str): The name of the decision which was evaluated.
        decision_definition_version (int): The version of the decision which was evaluated.
        decision_evaluation_key (str): The unique key identifying this decision evaluation. Example: 2251792362345323.
        decision_instance_key (str): Deprecated, please refer to `decisionEvaluationKey`. Example: 22517998136843567.
        decision_requirements_id (str): The ID of the decision requirements graph that the decision which was evaluated
            is part of.
        decision_requirements_key (str): The unique key identifying the decision requirements graph that the decision
            which was evaluated is part of. Example: 2251799813683346.
        evaluated_decisions (list[EvaluatedDecisionResult]): Decisions that were evaluated within the requested decision
            evaluation.
        failed_decision_definition_id (None | str): The ID of the decision which failed during evaluation. Example: new-
            hire-onboarding-workflow.
        failure_message (None | str): Message describing why the decision which was evaluated failed.
        output (str): JSON document that will instantiate the result of the decision which was evaluated.
        tenant_id (str): The tenant ID of the evaluated decision. Example: customer-service.
    """

    decision_definition_id: DecisionDefinitionId
    decision_definition_key: DecisionDefinitionKey
    decision_definition_name: str
    decision_definition_version: int
    decision_evaluation_key: DecisionEvaluationKey
    decision_instance_key: DecisionInstanceKey
    decision_requirements_id: str
    decision_requirements_key: DecisionRequirementsKey
    evaluated_decisions: list[EvaluatedDecisionResult]
    failed_decision_definition_id: None | DecisionDefinitionId
    failure_message: None | str
    output: str
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        decision_definition_key = self.decision_definition_key

        decision_definition_name = self.decision_definition_name

        decision_definition_version = self.decision_definition_version

        decision_evaluation_key = self.decision_evaluation_key

        decision_instance_key = self.decision_instance_key

        decision_requirements_id = self.decision_requirements_id

        decision_requirements_key = self.decision_requirements_key

        evaluated_decisions: list[dict[str, Any]] = []
        for evaluated_decisions_item_data in self.evaluated_decisions:
            evaluated_decisions_item = evaluated_decisions_item_data.to_dict()
            evaluated_decisions.append(evaluated_decisions_item)

        failed_decision_definition_id: None | DecisionDefinitionId
        failed_decision_definition_id = self.failed_decision_definition_id

        failure_message: None | str
        failure_message = self.failure_message

        output = self.output

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
                "decisionDefinitionKey": decision_definition_key,
                "decisionDefinitionName": decision_definition_name,
                "decisionDefinitionVersion": decision_definition_version,
                "decisionEvaluationKey": decision_evaluation_key,
                "decisionInstanceKey": decision_instance_key,
                "decisionRequirementsId": decision_requirements_id,
                "decisionRequirementsKey": decision_requirements_key,
                "evaluatedDecisions": evaluated_decisions,
                "failedDecisionDefinitionId": failed_decision_definition_id,
                "failureMessage": failure_message,
                "output": output,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluated_decision_result import EvaluatedDecisionResult

        d = dict(src_dict)
        decision_definition_id = lift_decision_definition_id(
            d.pop("decisionDefinitionId")
        )

        decision_definition_key = lift_decision_definition_key(
            d.pop("decisionDefinitionKey")
        )

        decision_definition_name = d.pop("decisionDefinitionName")

        decision_definition_version = d.pop("decisionDefinitionVersion")

        decision_evaluation_key = lift_decision_evaluation_key(
            d.pop("decisionEvaluationKey")
        )

        decision_instance_key = lift_decision_instance_key(d.pop("decisionInstanceKey"))

        decision_requirements_id = d.pop("decisionRequirementsId")

        decision_requirements_key = lift_decision_requirements_key(
            d.pop("decisionRequirementsKey")
        )

        evaluated_decisions: list[EvaluatedDecisionResult] = []
        _evaluated_decisions = d.pop("evaluatedDecisions")
        for evaluated_decisions_item_data in _evaluated_decisions:
            evaluated_decisions_item = EvaluatedDecisionResult.from_dict(
                evaluated_decisions_item_data
            )

            evaluated_decisions.append(evaluated_decisions_item)

        def _parse_failed_decision_definition_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_failed_decision_definition_id = _parse_failed_decision_definition_id(
            d.pop("failedDecisionDefinitionId")
        )

        failed_decision_definition_id = lift_decision_definition_id(
            _raw_failed_decision_definition_id
        )

        def _parse_failure_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_message = _parse_failure_message(d.pop("failureMessage"))

        output = d.pop("output")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        evaluate_decision_result = cls(
            decision_definition_id=decision_definition_id,
            decision_definition_key=decision_definition_key,
            decision_definition_name=decision_definition_name,
            decision_definition_version=decision_definition_version,
            decision_evaluation_key=decision_evaluation_key,
            decision_instance_key=decision_instance_key,
            decision_requirements_id=decision_requirements_id,
            decision_requirements_key=decision_requirements_key,
            evaluated_decisions=evaluated_decisions,
            failed_decision_definition_id=failed_decision_definition_id,
            failure_message=failure_message,
            output=output,
            tenant_id=tenant_id,
        )

        evaluate_decision_result.additional_properties = d
        return evaluate_decision_result

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
