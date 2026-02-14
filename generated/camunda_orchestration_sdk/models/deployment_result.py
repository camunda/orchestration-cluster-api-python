from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DeploymentKey,
    TenantId,
    lift_deployment_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.deployment_metadata_result import DeploymentMetadataResult


T = TypeVar("T", bound="DeploymentResult")


@_attrs_define
class DeploymentResult:
    """
    Attributes:
        deployment_key (str): The unique key identifying the deployment.
        tenant_id (str): The tenant ID associated with the deployment. Example: customer-service.
        deployments (list[DeploymentMetadataResult]): Items deployed by the request.
    """

    deployment_key: DeploymentKey
    tenant_id: TenantId
    deployments: list[DeploymentMetadataResult]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        deployment_key = self.deployment_key

        tenant_id = self.tenant_id

        deployments: list[dict[str, Any]] = []
        for deployments_item_data in self.deployments:
            deployments_item = deployments_item_data.to_dict()
            deployments.append(deployments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deploymentKey": deployment_key,
                "tenantId": tenant_id,
                "deployments": deployments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_metadata_result import DeploymentMetadataResult

        d = dict(src_dict)
        deployment_key = lift_deployment_key(d.pop("deploymentKey"))

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        deployments: list[DeploymentMetadataResult] = []
        _deployments = d.pop("deployments")
        for deployments_item_data in _deployments:
            deployments_item = DeploymentMetadataResult.from_dict(deployments_item_data)

            deployments.append(deployments_item)

        deployment_result = cls(
            deployment_key=deployment_key,
            tenant_id=tenant_id,
            deployments=deployments,
        )

        deployment_result.additional_properties = d
        return deployment_result

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
