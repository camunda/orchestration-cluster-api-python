from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionKey,
    TenantId,
    lift_decision_definition_key,
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


T = TypeVar("T", bound="DecisionEvaluationByKey")


@_attrs_define
class DecisionEvaluationByKey:
    """
    Attributes:
        decision_definition_key (str): System-generated key for a decision definition. Example: 2251799813326547.
        variables (DecisionEvaluationByIdVariables | Unset): The message variables as JSON document.
        tenant_id (str | Unset): The tenant ID of the decision. Example: customer-service.
    """

    decision_definition_key: DecisionDefinitionKey
    variables: DecisionEvaluationByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        decision_definition_key = self.decision_definition_key

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "decisionDefinitionKey": decision_definition_key,
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
        decision_definition_key = lift_decision_definition_key(
            d.pop("decisionDefinitionKey")
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

        decision_evaluation_by_key = cls(
            decision_definition_key=decision_definition_key,
            variables=variables,
            tenant_id=tenant_id,
        )

        return decision_evaluation_by_key
