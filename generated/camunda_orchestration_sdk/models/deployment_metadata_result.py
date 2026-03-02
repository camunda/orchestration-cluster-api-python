from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.deployment_metadata_result_decision_definition import (
        DeploymentMetadataResultDecisionDefinition,
    )
    from ..models.deployment_metadata_result_decision_requirements import (
        DeploymentMetadataResultDecisionRequirements,
    )
    from ..models.deployment_metadata_result_form import DeploymentMetadataResultForm
    from ..models.deployment_metadata_result_process_definition import (
        DeploymentMetadataResultProcessDefinition,
    )
    from ..models.deployment_metadata_result_resource import (
        DeploymentMetadataResultResource,
    )


T = TypeVar("T", bound="DeploymentMetadataResult")


@_attrs_define
class DeploymentMetadataResult:
    """
    Attributes:
        process_definition (DeploymentMetadataResultProcessDefinition | None | Unset): Deployed process.
        decision_definition (DeploymentMetadataResultDecisionDefinition | None | Unset): Deployed decision.
        decision_requirements (DeploymentMetadataResultDecisionRequirements | None | Unset): Deployed decision
            requirement definition.
        form (DeploymentMetadataResultForm | None | Unset): Deployed form.
        resource (DeploymentMetadataResultResource | None | Unset): Deployed resource.
    """

    process_definition: DeploymentMetadataResultProcessDefinition | None | Unset = UNSET
    decision_definition: DeploymentMetadataResultDecisionDefinition | None | Unset = (
        UNSET
    )
    decision_requirements: (
        DeploymentMetadataResultDecisionRequirements | None | Unset
    ) = UNSET
    form: DeploymentMetadataResultForm | None | Unset = UNSET
    resource: DeploymentMetadataResultResource | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.deployment_metadata_result_decision_definition import (
            DeploymentMetadataResultDecisionDefinition,
        )
        from ..models.deployment_metadata_result_decision_requirements import (
            DeploymentMetadataResultDecisionRequirements,
        )
        from ..models.deployment_metadata_result_form import (
            DeploymentMetadataResultForm,
        )
        from ..models.deployment_metadata_result_process_definition import (
            DeploymentMetadataResultProcessDefinition,
        )
        from ..models.deployment_metadata_result_resource import (
            DeploymentMetadataResultResource,
        )

        process_definition: dict[str, Any] | None | Unset
        if isinstance(self.process_definition, Unset):
            process_definition = UNSET
        elif isinstance(
            self.process_definition, DeploymentMetadataResultProcessDefinition
        ):
            process_definition = self.process_definition.to_dict()
        else:
            process_definition = self.process_definition

        decision_definition: dict[str, Any] | None | Unset
        if isinstance(self.decision_definition, Unset):
            decision_definition = UNSET
        elif isinstance(
            self.decision_definition, DeploymentMetadataResultDecisionDefinition
        ):
            decision_definition = self.decision_definition.to_dict()
        else:
            decision_definition = self.decision_definition

        decision_requirements: dict[str, Any] | None | Unset
        if isinstance(self.decision_requirements, Unset):
            decision_requirements = UNSET
        elif isinstance(
            self.decision_requirements, DeploymentMetadataResultDecisionRequirements
        ):
            decision_requirements = self.decision_requirements.to_dict()
        else:
            decision_requirements = self.decision_requirements

        form: dict[str, Any] | None | Unset
        if isinstance(self.form, Unset):
            form = UNSET
        elif isinstance(self.form, DeploymentMetadataResultForm):
            form = self.form.to_dict()
        else:
            form = self.form

        resource: dict[str, Any] | None | Unset
        if isinstance(self.resource, Unset):
            resource = UNSET
        elif isinstance(self.resource, DeploymentMetadataResultResource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource

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
        from ..models.deployment_metadata_result_decision_definition import (
            DeploymentMetadataResultDecisionDefinition,
        )
        from ..models.deployment_metadata_result_decision_requirements import (
            DeploymentMetadataResultDecisionRequirements,
        )
        from ..models.deployment_metadata_result_form import (
            DeploymentMetadataResultForm,
        )
        from ..models.deployment_metadata_result_process_definition import (
            DeploymentMetadataResultProcessDefinition,
        )
        from ..models.deployment_metadata_result_resource import (
            DeploymentMetadataResultResource,
        )

        d = dict(src_dict)

        def _parse_process_definition(
            data: object,
        ) -> DeploymentMetadataResultProcessDefinition | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_deployment_metadata_result_process_definition_type_0 = DeploymentMetadataResultProcessDefinition.from_dict(
                    data
                )

                return componentsschemas_deployment_metadata_result_process_definition_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeploymentMetadataResultProcessDefinition | None | Unset, data)

        process_definition = _parse_process_definition(
            d.pop("processDefinition", UNSET)
        )

        def _parse_decision_definition(
            data: object,
        ) -> DeploymentMetadataResultDecisionDefinition | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_deployment_metadata_result_decision_definition_type_0 = DeploymentMetadataResultDecisionDefinition.from_dict(
                    data
                )

                return componentsschemas_deployment_metadata_result_decision_definition_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeploymentMetadataResultDecisionDefinition | None | Unset, data)

        decision_definition = _parse_decision_definition(
            d.pop("decisionDefinition", UNSET)
        )

        def _parse_decision_requirements(
            data: object,
        ) -> DeploymentMetadataResultDecisionRequirements | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_deployment_metadata_result_decision_requirements_type_0 = DeploymentMetadataResultDecisionRequirements.from_dict(
                    data
                )

                return componentsschemas_deployment_metadata_result_decision_requirements_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DeploymentMetadataResultDecisionRequirements | None | Unset, data
            )

        decision_requirements = _parse_decision_requirements(
            d.pop("decisionRequirements", UNSET)
        )

        def _parse_form(data: object) -> DeploymentMetadataResultForm | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_deployment_metadata_result_form_type_0 = (
                    DeploymentMetadataResultForm.from_dict(data)
                )

                return componentsschemas_deployment_metadata_result_form_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeploymentMetadataResultForm | None | Unset, data)

        form = _parse_form(d.pop("form", UNSET))

        def _parse_resource(
            data: object,
        ) -> DeploymentMetadataResultResource | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_deployment_metadata_result_resource_type_0 = (
                    DeploymentMetadataResultResource.from_dict(data)
                )

                return componentsschemas_deployment_metadata_result_resource_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeploymentMetadataResultResource | None | Unset, data)

        resource = _parse_resource(d.pop("resource", UNSET))

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
