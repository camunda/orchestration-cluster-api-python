from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionRequirementsKey,
    TenantId,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeploymentDecisionResult")


@_attrs_define
class DeploymentDecisionResult:
    """A deployed decision.

    Attributes:
        decision_definition_id (str): The dmn decision ID, as parsed during deployment, together with the version forms
            a
            unique identifier for a specific decision.
             Example: new-hire-onboarding-workflow.
        version (int): The assigned decision version.
        name (str): The DMN name of the decision, as parsed during deployment.
        tenant_id (str): The tenant ID of the deployed decision. Example: customer-service.
        decision_requirements_id (str): The dmn ID of the decision requirements graph that this decision is part of, as
            parsed during deployment.
        decision_definition_key (str): The assigned decision key, which acts as a unique identifier for this decision.
             Example: 2251799813326547.
        decision_requirements_key (str): The assigned key of the decision requirements graph that this decision is part
            of.
             Example: 2251799813683346.
    """

    decision_definition_id: DecisionDefinitionId
    version: int
    name: str
    tenant_id: TenantId
    decision_requirements_id: str
    decision_definition_key: DecisionDefinitionKey
    decision_requirements_key: DecisionRequirementsKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        version = self.version

        name = self.name

        tenant_id = self.tenant_id

        decision_requirements_id = self.decision_requirements_id

        decision_definition_key = self.decision_definition_key

        decision_requirements_key = self.decision_requirements_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
                "version": version,
                "name": name,
                "tenantId": tenant_id,
                "decisionRequirementsId": decision_requirements_id,
                "decisionDefinitionKey": decision_definition_key,
                "decisionRequirementsKey": decision_requirements_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_definition_id = DecisionDefinitionId(d.pop("decisionDefinitionId"))

        version = d.pop("version")

        name = d.pop("name")

        tenant_id = TenantId(d.pop("tenantId"))

        decision_requirements_id = d.pop("decisionRequirementsId")

        decision_definition_key = DecisionDefinitionKey(d.pop("decisionDefinitionKey"))

        decision_requirements_key = DecisionRequirementsKey(
            d.pop("decisionRequirementsKey")
        )

        deployment_decision_result = cls(
            decision_definition_id=decision_definition_id,
            version=version,
            name=name,
            tenant_id=tenant_id,
            decision_requirements_id=decision_requirements_id,
            decision_definition_key=decision_definition_key,
            decision_requirements_key=decision_requirements_key,
        )

        deployment_decision_result.additional_properties = d
        return deployment_decision_result

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
