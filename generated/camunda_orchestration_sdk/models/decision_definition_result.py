from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionRequirementsKey,
    TenantId,
    lift_decision_definition_id,
    lift_decision_definition_key,
    lift_decision_requirements_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DecisionDefinitionResult")


@_attrs_define
class DecisionDefinitionResult:
    """
    Attributes:
        decision_definition_id (str): The DMN ID of the decision definition. Example: new-hire-onboarding-workflow.
        decision_definition_key (str): The assigned key, which acts as a unique identifier for this decision definition.
            Example: 2251799813326547.
        decision_requirements_id (str): the DMN ID of the decision requirements graph that the decision definition is
            part of.
        decision_requirements_key (str): The assigned key of the decision requirements graph that the decision
            definition is part of. Example: 2251799813683346.
        decision_requirements_name (str): The DMN name of the decision requirements that the decision definition is part
            of.
        decision_requirements_version (int): The assigned version of the decision requirements that the decision
            definition is part of.
        name (str): The DMN name of the decision definition.
        tenant_id (str): The tenant ID of the decision definition. Example: customer-service.
        version (int): The assigned version of the decision definition.
    """

    decision_definition_id: DecisionDefinitionId
    decision_definition_key: DecisionDefinitionKey
    decision_requirements_id: str
    decision_requirements_key: DecisionRequirementsKey
    decision_requirements_name: str
    decision_requirements_version: int
    name: str
    tenant_id: TenantId
    version: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        decision_definition_key = self.decision_definition_key

        decision_requirements_id = self.decision_requirements_id

        decision_requirements_key = self.decision_requirements_key

        decision_requirements_name = self.decision_requirements_name

        decision_requirements_version = self.decision_requirements_version

        name = self.name

        tenant_id = self.tenant_id

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
                "decisionDefinitionKey": decision_definition_key,
                "decisionRequirementsId": decision_requirements_id,
                "decisionRequirementsKey": decision_requirements_key,
                "decisionRequirementsName": decision_requirements_name,
                "decisionRequirementsVersion": decision_requirements_version,
                "name": name,
                "tenantId": tenant_id,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_definition_id = lift_decision_definition_id(
            d.pop("decisionDefinitionId")
        )

        decision_definition_key = lift_decision_definition_key(
            d.pop("decisionDefinitionKey")
        )

        decision_requirements_id = d.pop("decisionRequirementsId")

        decision_requirements_key = lift_decision_requirements_key(
            d.pop("decisionRequirementsKey")
        )

        decision_requirements_name = d.pop("decisionRequirementsName")

        decision_requirements_version = d.pop("decisionRequirementsVersion")

        name = d.pop("name")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        version = d.pop("version")

        decision_definition_result = cls(
            decision_definition_id=decision_definition_id,
            decision_definition_key=decision_definition_key,
            decision_requirements_id=decision_requirements_id,
            decision_requirements_key=decision_requirements_key,
            decision_requirements_name=decision_requirements_name,
            decision_requirements_version=decision_requirements_version,
            name=name,
            tenant_id=tenant_id,
            version=version,
        )

        decision_definition_result.additional_properties = d
        return decision_definition_result

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
