from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="GetGlobalJobStatisticsResponse200Created")


@_attrs_define
class GetGlobalJobStatisticsResponse200Created:
    """Metric for a single job status.

    Attributes:
        count (int): Number of jobs in this status. Example: 145.
        last_updated_at (datetime.datetime): ISO 8601 timestamp of the last update for this status. Example:
            2024-07-29T15:51:28.071Z.
    """

    count: int
    last_updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        last_updated_at = self.last_updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "lastUpdatedAt": last_updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        last_updated_at = isoparse(d.pop("lastUpdatedAt"))

        get_global_job_statistics_response_200_created = cls(
            count=count,
            last_updated_at=last_updated_at,
        )

        get_global_job_statistics_response_200_created.additional_properties = d
        return get_global_job_statistics_response_200_created

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
