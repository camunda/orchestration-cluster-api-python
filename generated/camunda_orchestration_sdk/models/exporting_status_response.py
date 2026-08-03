from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.exporting_status_response_exporting_status_code import (
    ExportingStatusResponseExportingStatusCode,
)

T = TypeVar("T", bound="ExportingStatusResponse")


@_attrs_define
class ExportingStatusResponse:
    """Response body for the exporting status of a physical tenant.

    Attributes:
        status (ExportingStatusResponseExportingStatusCode): The aggregated exporting status of the physical tenant.
            Example: PAUSED.
    """

    status: ExportingStatusResponseExportingStatusCode
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ExportingStatusResponseExportingStatusCode(d.pop("status"))

        exporting_status_response = cls(
            status=status,
        )

        exporting_status_response.additional_properties = d
        return exporting_status_response

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
