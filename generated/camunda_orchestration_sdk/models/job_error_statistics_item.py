from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="JobErrorStatisticsItem")


@_attrs_define
class JobErrorStatisticsItem:
    """Aggregated error metrics for a single error type and message combination.

    Attributes:
        error_code (str): The error code identifier. Example: UNHANDLED_ERROR_EVENT.
        error_message (str): The error message. Example: An unexpected error occurred..
        workers (int): Number of distinct workers that encountered this error. Example: 15.
    """

    error_code: str
    error_message: str
    workers: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        error_code = self.error_code

        error_message = self.error_message

        workers = self.workers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errorCode": error_code,
                "errorMessage": error_message,
                "workers": workers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error_code = d.pop("errorCode")

        error_message = d.pop("errorMessage")

        workers = d.pop("workers")

        job_error_statistics_item = cls(
            error_code=error_code,
            error_message=error_message,
            workers=workers,
        )

        job_error_statistics_item.additional_properties = d
        return job_error_statistics_item

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
