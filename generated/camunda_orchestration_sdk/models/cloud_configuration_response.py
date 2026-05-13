from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cloud_configuration_response_stage import CloudConfigurationResponseStage

T = TypeVar("T", bound="CloudConfigurationResponse")


@_attrs_define
class CloudConfigurationResponse:
    """Configuration for SaaS/cloud-specific settings.

    Attributes:
        organization_id (None | str): The SaaS organization ID, if applicable. Example: org-123456.
        cluster_id (None | str): The SaaS cluster ID, if applicable. Example: cluster-abc.
        stage (CloudConfigurationResponseStage): The cloud deployment stage. Example: prod.
        mixpanel_token (None | str): The Mixpanel analytics token for the cloud UI. Example: abc123token.
        mixpanel_api_host (None | str): The Mixpanel API host URL. Example: https://api.mixpanel.com.
    """

    organization_id: None | str
    cluster_id: None | str
    stage: CloudConfigurationResponseStage
    mixpanel_token: None | str
    mixpanel_api_host: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        organization_id: None | str
        organization_id = self.organization_id

        cluster_id: None | str
        cluster_id = self.cluster_id

        stage = self.stage.value

        mixpanel_token: None | str
        mixpanel_token = self.mixpanel_token

        mixpanel_api_host: None | str
        mixpanel_api_host = self.mixpanel_api_host

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organizationId": organization_id,
                "clusterId": cluster_id,
                "stage": stage,
                "mixpanelToken": mixpanel_token,
                "mixpanelAPIHost": mixpanel_api_host,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_organization_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization_id = _parse_organization_id(d.pop("organizationId"))

        def _parse_cluster_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cluster_id = _parse_cluster_id(d.pop("clusterId"))

        stage = CloudConfigurationResponseStage(d.pop("stage"))

        def _parse_mixpanel_token(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mixpanel_token = _parse_mixpanel_token(d.pop("mixpanelToken"))

        def _parse_mixpanel_api_host(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mixpanel_api_host = _parse_mixpanel_api_host(d.pop("mixpanelAPIHost"))

        cloud_configuration_response = cls(
            organization_id=organization_id,
            cluster_id=cluster_id,
            stage=stage,
            mixpanel_token=mixpanel_token,
            mixpanel_api_host=mixpanel_api_host,
        )

        cloud_configuration_response.additional_properties = d
        return cloud_configuration_response

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
