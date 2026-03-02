from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

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
        process_definition (DeploymentMetadataResultProcessDefinition | None): Deployed process.
        decision_definition (DeploymentMetadataResultDecisionDefinition | None): Deployed decision.
        decision_requirements (DeploymentMetadataResultDecisionRequirements | None): Deployed decision requirement
            definition.
        form (DeploymentMetadataResultForm | None): Deployed form.
        resource (DeploymentMetadataResultResource | None): Deployed resource.
    """

    process_definition: DeploymentMetadataResultProcessDefinition | None
    decision_definition: DeploymentMetadataResultDecisionDefinition | None
    decision_requirements: DeploymentMetadataResultDecisionRequirements | None
    form: DeploymentMetadataResultForm | None
    resource: DeploymentMetadataResultResource | None
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

        process_definition: dict[str, Any] | None
        if isinstance(
            self.process_definition, DeploymentMetadataResultProcessDefinition
        ):
            process_definition = self.process_definition.to_dict()
        else:
            process_definition = self.process_definition

        decision_definition: dict[str, Any] | None
        if isinstance(
            self.decision_definition, DeploymentMetadataResultDecisionDefinition
        ):
            decision_definition = self.decision_definition.to_dict()
        else:
            decision_definition = self.decision_definition

        decision_requirements: dict[str, Any] | None
        if isinstance(
            self.decision_requirements, DeploymentMetadataResultDecisionRequirements
        ):
            decision_requirements = self.decision_requirements.to_dict()
        else:
            decision_requirements = self.decision_requirements

        form: dict[str, Any] | None
        if isinstance(self.form, DeploymentMetadataResultForm):
            form = self.form.to_dict()
        else:
            form = self.form

        resource: dict[str, Any] | None
        if isinstance(self.resource, DeploymentMetadataResultResource):
            resource = self.resource.to_dict()
        else:
            resource = self.resource

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinition": process_definition,
                "decisionDefinition": decision_definition,
                "decisionRequirements": decision_requirements,
                "form": form,
                "resource": resource,
            }
        )

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
        ) -> DeploymentMetadataResultProcessDefinition | None:
            if data is None:
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
            return cast(DeploymentMetadataResultProcessDefinition | None, data)

        process_definition = _parse_process_definition(d.pop("processDefinition"))

        def _parse_decision_definition(
            data: object,
        ) -> DeploymentMetadataResultDecisionDefinition | None:
            if data is None:
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
            return cast(DeploymentMetadataResultDecisionDefinition | None, data)

        decision_definition = _parse_decision_definition(d.pop("decisionDefinition"))

        def _parse_decision_requirements(
            data: object,
        ) -> DeploymentMetadataResultDecisionRequirements | None:
            if data is None:
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
            return cast(DeploymentMetadataResultDecisionRequirements | None, data)

        decision_requirements = _parse_decision_requirements(
            d.pop("decisionRequirements")
        )

        def _parse_form(data: object) -> DeploymentMetadataResultForm | None:
            if data is None:
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
            return cast(DeploymentMetadataResultForm | None, data)

        form = _parse_form(d.pop("form"))

        def _parse_resource(data: object) -> DeploymentMetadataResultResource | None:
            if data is None:
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
            return cast(DeploymentMetadataResultResource | None, data)

        resource = _parse_resource(d.pop("resource"))

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
