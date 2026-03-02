from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.deployment_metadata_result_decision_definition import DeploymentMetadataResultDecisionDefinition
from ..models.deployment_metadata_result_decision_requirements import DeploymentMetadataResultDecisionRequirements
from ..models.deployment_metadata_result_form import DeploymentMetadataResultForm
from ..models.deployment_metadata_result_process_definition import DeploymentMetadataResultProcessDefinition
from ..models.deployment_metadata_result_resource import DeploymentMetadataResultResource
T = TypeVar("T", bound="DeploymentMetadataResult")
@_attrs_define
class DeploymentMetadataResult:
    process_definition: DeploymentMetadataResultProcessDefinition | None | Unset = UNSET
    decision_definition: DeploymentMetadataResultDecisionDefinition | None | Unset = (
            UNSET
        )
    decision_requirements: (
            DeploymentMetadataResultDecisionRequirements | None | Unset
        ) = UNSET
    form: DeploymentMetadataResultForm | None | Unset = UNSET
    resource: DeploymentMetadataResultResource | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
