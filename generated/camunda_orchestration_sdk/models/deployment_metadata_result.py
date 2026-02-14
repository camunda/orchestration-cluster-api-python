from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.deployment_decision_requirements_result import (
        DeploymentDecisionRequirementsResult,
    )
    from ..models.deployment_decision_result import DeploymentDecisionResult
    from ..models.deployment_form_result import DeploymentFormResult
    from ..models.deployment_process_result import DeploymentProcessResult
    from ..models.deployment_resource_result import DeploymentResourceResult


T = TypeVar("T", bound="DeploymentMetadataResult")


@_attrs_define
class DeploymentMetadataResult:
    """
    Attributes:
        process_definition (DeploymentProcessResult | Unset): A deployed process.
        decision_definition (DeploymentDecisionResult | Unset): A deployed decision.
        decision_requirements (DeploymentDecisionRequirementsResult | Unset): Deployed decision requirements.
        form (DeploymentFormResult | Unset): A deployed form.
        resource (DeploymentResourceResult | Unset): A deployed Resource.
    """

    process_definition: DeploymentProcessResult | Unset = UNSET
    decision_definition: DeploymentDecisionResult | Unset = UNSET
    decision_requirements: DeploymentDecisionRequirementsResult | Unset = UNSET
    form: DeploymentFormResult | Unset = UNSET
    resource: DeploymentResourceResult | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition: dict[str, Any] | Unset = UNSET
        if not isinstance(self.process_definition, Unset):
            process_definition = self.process_definition.to_dict()

        decision_definition: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decision_definition, Unset):
            decision_definition = self.decision_definition.to_dict()

        decision_requirements: dict[str, Any] | Unset = UNSET
        if not isinstance(self.decision_requirements, Unset):
            decision_requirements = self.decision_requirements.to_dict()

        form: dict[str, Any] | Unset = UNSET
        if not isinstance(self.form, Unset):
            form = self.form.to_dict()

        resource: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if process_definition is not UNSET:
            field_dict["processDefinition"] = process_definition
        if decision_definition is not UNSET:
            field_dict["decisionDefinition"] = decision_definition
        if decision_requirements is not UNSET:
            field_dict["decisionRequirements"] = decision_requirements
        if form is not UNSET:
            field_dict["form"] = form
        if resource is not UNSET:
            field_dict["resource"] = resource

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deployment_decision_requirements_result import (
            DeploymentDecisionRequirementsResult,
        )
        from ..models.deployment_decision_result import DeploymentDecisionResult
        from ..models.deployment_form_result import DeploymentFormResult
        from ..models.deployment_process_result import DeploymentProcessResult
        from ..models.deployment_resource_result import DeploymentResourceResult

        d = dict(src_dict)
        _process_definition = d.pop("processDefinition", UNSET)
        process_definition: DeploymentProcessResult | Unset
        if isinstance(_process_definition, Unset):
            process_definition = UNSET
        else:
            process_definition = DeploymentProcessResult.from_dict(_process_definition)

        _decision_definition = d.pop("decisionDefinition", UNSET)
        decision_definition: DeploymentDecisionResult | Unset
        if isinstance(_decision_definition, Unset):
            decision_definition = UNSET
        else:
            decision_definition = DeploymentDecisionResult.from_dict(
                _decision_definition
            )

        _decision_requirements = d.pop("decisionRequirements", UNSET)
        decision_requirements: DeploymentDecisionRequirementsResult | Unset
        if isinstance(_decision_requirements, Unset):
            decision_requirements = UNSET
        else:
            decision_requirements = DeploymentDecisionRequirementsResult.from_dict(
                _decision_requirements
            )

        _form = d.pop("form", UNSET)
        form: DeploymentFormResult | Unset
        if isinstance(_form, Unset):
            form = UNSET
        else:
            form = DeploymentFormResult.from_dict(_form)

        _resource = d.pop("resource", UNSET)
        resource: DeploymentResourceResult | Unset
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = DeploymentResourceResult.from_dict(_resource)

        deployment_metadata_result = cls(
            process_definition=process_definition,
            decision_definition=decision_definition,
            decision_requirements=decision_requirements,
            form=form,
            resource=resource,
        )

        deployment_metadata_result.additional_properties = d
        return deployment_metadata_result

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
