from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.authentication_configuration_response import (
        AuthenticationConfigurationResponse,
    )
    from ..models.cloud_configuration_response import CloudConfigurationResponse
    from ..models.components_configuration_response import (
        ComponentsConfigurationResponse,
    )
    from ..models.deployment_configuration_response import (
        DeploymentConfigurationResponse,
    )
    from ..models.job_metrics_configuration_response import (
        JobMetricsConfigurationResponse,
    )


T = TypeVar("T", bound="SystemConfigurationResponse")


@_attrs_define
class SystemConfigurationResponse:
    """Envelope for all system configuration sections. Each property
    represents a feature area.

        Attributes:
            job_metrics (JobMetricsConfigurationResponse): Configuration for job metrics collection and export.
            components (ComponentsConfigurationResponse): Configuration for active Camunda components in the deployment.
            deployment (DeploymentConfigurationResponse): Configuration for deployment characteristics.
            authentication (AuthenticationConfigurationResponse): Configuration for authentication and session management.
            cloud (CloudConfigurationResponse): Configuration for SaaS/cloud-specific settings.
    """

    job_metrics: JobMetricsConfigurationResponse
    components: ComponentsConfigurationResponse
    deployment: DeploymentConfigurationResponse
    authentication: AuthenticationConfigurationResponse
    cloud: CloudConfigurationResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        job_metrics = self.job_metrics.to_dict()

        components = self.components.to_dict()

        deployment = self.deployment.to_dict()

        authentication = self.authentication.to_dict()

        cloud = self.cloud.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobMetrics": job_metrics,
                "components": components,
                "deployment": deployment,
                "authentication": authentication,
                "cloud": cloud,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.authentication_configuration_response import (
            AuthenticationConfigurationResponse,
        )
        from ..models.cloud_configuration_response import CloudConfigurationResponse
        from ..models.components_configuration_response import (
            ComponentsConfigurationResponse,
        )
        from ..models.deployment_configuration_response import (
            DeploymentConfigurationResponse,
        )
        from ..models.job_metrics_configuration_response import (
            JobMetricsConfigurationResponse,
        )

        d = dict(src_dict)
        job_metrics = JobMetricsConfigurationResponse.from_dict(d.pop("jobMetrics"))

        components = ComponentsConfigurationResponse.from_dict(d.pop("components"))

        deployment = DeploymentConfigurationResponse.from_dict(d.pop("deployment"))

        authentication = AuthenticationConfigurationResponse.from_dict(
            d.pop("authentication")
        )

        cloud = CloudConfigurationResponse.from_dict(d.pop("cloud"))

        system_configuration_response = cls(
            job_metrics=job_metrics,
            components=components,
            deployment=deployment,
            authentication=authentication,
            cloud=cloud,
        )

        system_configuration_response.additional_properties = d
        return system_configuration_response

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
