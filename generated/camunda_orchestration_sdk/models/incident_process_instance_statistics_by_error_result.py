from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="IncidentProcessInstanceStatisticsByErrorResult")


@_attrs_define
class IncidentProcessInstanceStatisticsByErrorResult:
    """
    Attributes:
        error_hash_code (int): The hash code identifying a specific incident error..
        error_message (str): The error message associated with the incident error hash code.
        active_instances_with_error_count (int): The number of active process instances that currently have an active
            incident with this error.
    """

    error_hash_code: int
    error_message: str
    active_instances_with_error_count: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        error_hash_code = self.error_hash_code

        error_message = self.error_message

        active_instances_with_error_count = self.active_instances_with_error_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errorHashCode": error_hash_code,
                "errorMessage": error_message,
                "activeInstancesWithErrorCount": active_instances_with_error_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error_hash_code = d.pop("errorHashCode")

        error_message = d.pop("errorMessage")

        active_instances_with_error_count = d.pop("activeInstancesWithErrorCount")

        incident_process_instance_statistics_by_error_result = cls(
            error_hash_code=error_hash_code,
            error_message=error_message,
            active_instances_with_error_count=active_instances_with_error_count,
        )

        incident_process_instance_statistics_by_error_result.additional_properties = d
        return incident_process_instance_statistics_by_error_result

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
