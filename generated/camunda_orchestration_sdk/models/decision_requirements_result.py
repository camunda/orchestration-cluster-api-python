from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import DecisionRequirementsKey, TenantId

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DecisionRequirementsResult")


@_attrs_define
class DecisionRequirementsResult:
    """
    Attributes:
        decision_requirements_id (str): The DMN ID of the decision requirements.
        decision_requirements_key (str): The assigned key, which acts as a unique identifier for this decision
            requirements. Example: 2251799813683346.
        decision_requirements_name (str): The DMN name of the decision requirements.
        resource_name (str): The name of the resource from which this decision requirements was parsed.
        tenant_id (str): The tenant ID of the decision requirements. Example: customer-service.
        version (int): The assigned version of the decision requirements.
    """

    decision_requirements_id: str
    decision_requirements_key: DecisionRequirementsKey
    decision_requirements_name: str
    resource_name: str
    tenant_id: TenantId
    version: int

    def to_dict(self) -> dict[str, Any]:
        decision_requirements_id = self.decision_requirements_id

        decision_requirements_key = self.decision_requirements_key

        decision_requirements_name = self.decision_requirements_name

        resource_name = self.resource_name

        tenant_id = self.tenant_id

        version = self.version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "decisionRequirementsId": decision_requirements_id,
                "decisionRequirementsKey": decision_requirements_key,
                "decisionRequirementsName": decision_requirements_name,
                "resourceName": resource_name,
                "tenantId": tenant_id,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_requirements_id = d.pop("decisionRequirementsId")

        decision_requirements_key = DecisionRequirementsKey(
            d.pop("decisionRequirementsKey")
        )

        decision_requirements_name = d.pop("decisionRequirementsName")

        resource_name = d.pop("resourceName")

        tenant_id = TenantId(d.pop("tenantId"))

        version = d.pop("version")

        decision_requirements_result = cls(
            decision_requirements_id=decision_requirements_id,
            decision_requirements_key=decision_requirements_key,
            decision_requirements_name=decision_requirements_name,
            resource_name=resource_name,
            tenant_id=tenant_id,
            version=version,
        )

        return decision_requirements_result
