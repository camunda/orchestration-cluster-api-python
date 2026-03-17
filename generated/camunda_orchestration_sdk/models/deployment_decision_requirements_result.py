from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionRequirementsKey,
    TenantId,
    lift_decision_requirements_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeploymentDecisionRequirementsResult")


@_attrs_define
class DeploymentDecisionRequirementsResult:
    """Deployed decision requirements.

    Attributes:
        decision_requirements_id (str): The id of the deployed decision requirements.
        decision_requirements_name (str): The name of the deployed decision requirements.
        version (int): The version of the deployed decision requirements.
        resource_name (str): The name of the resource.
        tenant_id (str): The tenant ID of the deployed decision requirements. Example: customer-service.
        decision_requirements_key (str): The assigned decision requirements key, which acts as a unique identifier for
            this decision requirements.
             Example: 2251799813683346.
    """

    decision_requirements_id: str
    decision_requirements_name: str
    version: int
    resource_name: str
    tenant_id: TenantId
    decision_requirements_key: DecisionRequirementsKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_requirements_id = self.decision_requirements_id

        decision_requirements_name = self.decision_requirements_name

        version = self.version

        resource_name = self.resource_name

        tenant_id = self.tenant_id

        decision_requirements_key = self.decision_requirements_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionRequirementsId": decision_requirements_id,
                "decisionRequirementsName": decision_requirements_name,
                "version": version,
                "resourceName": resource_name,
                "tenantId": tenant_id,
                "decisionRequirementsKey": decision_requirements_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_requirements_id = d.pop("decisionRequirementsId")

        decision_requirements_name = d.pop("decisionRequirementsName")

        version = d.pop("version")

        resource_name = d.pop("resourceName")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        decision_requirements_key = lift_decision_requirements_key(
            d.pop("decisionRequirementsKey")
        )

        deployment_decision_requirements_result = cls(
            decision_requirements_id=decision_requirements_id,
            decision_requirements_name=decision_requirements_name,
            version=version,
            resource_name=resource_name,
            tenant_id=tenant_id,
            decision_requirements_key=decision_requirements_key,
        )

        deployment_decision_requirements_result.additional_properties = d
        return deployment_decision_requirements_result

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
