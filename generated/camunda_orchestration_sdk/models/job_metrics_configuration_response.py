from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="JobMetricsConfigurationResponse")


@_attrs_define
class JobMetricsConfigurationResponse:
    """Configuration for job metrics collection and export.

    Attributes:
        enabled (bool): Whether job metrics export is enabled. Example: True.
        export_interval (str): The interval at which job metrics are exported, as an ISO 8601 duration. Example: PT5M.
        max_worker_name_length (int): The maximum length of the worker name used in job metrics labels. Example: 100.
        max_job_type_length (int): The maximum length of the job type used in job metrics labels. Example: 100.
        max_tenant_id_length (int): The maximum length of the tenant ID used in job metrics labels. Example: 30.
        max_unique_keys (int): The maximum number of unique metric keys tracked for job metrics. Example: 9500.
    """

    enabled: bool
    export_interval: str
    max_worker_name_length: int
    max_job_type_length: int
    max_tenant_id_length: int
    max_unique_keys: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        export_interval = self.export_interval

        max_worker_name_length = self.max_worker_name_length

        max_job_type_length = self.max_job_type_length

        max_tenant_id_length = self.max_tenant_id_length

        max_unique_keys = self.max_unique_keys

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "exportInterval": export_interval,
                "maxWorkerNameLength": max_worker_name_length,
                "maxJobTypeLength": max_job_type_length,
                "maxTenantIdLength": max_tenant_id_length,
                "maxUniqueKeys": max_unique_keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        export_interval = d.pop("exportInterval")

        max_worker_name_length = d.pop("maxWorkerNameLength")

        max_job_type_length = d.pop("maxJobTypeLength")

        max_tenant_id_length = d.pop("maxTenantIdLength")

        max_unique_keys = d.pop("maxUniqueKeys")

        job_metrics_configuration_response = cls(
            enabled=enabled,
            export_interval=export_interval,
            max_worker_name_length=max_worker_name_length,
            max_job_type_length=max_job_type_length,
            max_tenant_id_length=max_tenant_id_length,
            max_unique_keys=max_unique_keys,
        )

        job_metrics_configuration_response.additional_properties = d
        return job_metrics_configuration_response

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
