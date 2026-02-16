from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.deployment_decision_requirements_result import (
    DeploymentDecisionRequirementsResult,
)
from ..models.deployment_decision_result import DeploymentDecisionResult
from ..models.deployment_form_result import DeploymentFormResult
from ..models.deployment_process_result import DeploymentProcessResult
from ..models.deployment_resource_result import DeploymentResourceResult

T = TypeVar("T", bound="CreateDeploymentDeploymentsItem")

@_attrs_define
class CreateDeploymentDeploymentsItem:
    process_definition: DeploymentProcessResult | Unset = UNSET
    decision_definition: DeploymentDecisionResult | Unset = UNSET
    decision_requirements: DeploymentDecisionRequirementsResult | Unset = UNSET
    form: DeploymentFormResult | Unset = UNSET
    resource: DeploymentResourceResult | Unset = UNSET
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
