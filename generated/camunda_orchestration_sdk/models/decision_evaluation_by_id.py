from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    TenantId,
    lift_decision_definition_id,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_evaluation_by_id_variables import (
        DecisionEvaluationByIdVariables,
    )


T = TypeVar("T", bound="DecisionEvaluationByID")


@_attrs_define
class DecisionEvaluationByID:
    """
    Attributes:
        decision_definition_id (str): The ID of the decision to be evaluated.
            When using the decision ID, the latest
            deployed version of the decision is used.
             Example: new-hire-onboarding-workflow.
        variables (DecisionEvaluationByIdVariables | Unset): The message variables as JSON document.
        tenant_id (str | Unset): The tenant ID of the decision. Example: customer-service.
    """

    decision_definition_id: DecisionDefinitionId
    variables: DecisionEvaluationByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_evaluation_by_id_variables import (
            DecisionEvaluationByIdVariables,
        )

        d = dict(src_dict)
        decision_definition_id = lift_decision_definition_id(
            d.pop("decisionDefinitionId")
        )

        _variables = d.pop("variables", UNSET)
        variables: DecisionEvaluationByIdVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = DecisionEvaluationByIdVariables.from_dict(_variables)

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        decision_evaluation_by_id = cls(
            decision_definition_id=decision_definition_id,
            variables=variables,
            tenant_id=tenant_id,
        )

        return decision_evaluation_by_id
