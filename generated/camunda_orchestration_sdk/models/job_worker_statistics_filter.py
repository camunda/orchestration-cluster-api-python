from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="JobWorkerStatisticsFilter")


@_attrs_define
class JobWorkerStatisticsFilter:
    """Job worker statistics search filter.

    Attributes:
        from_ (datetime.datetime): Start of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-28T15:51:28.071Z.
        to (datetime.datetime): End of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-29T15:51:28.071Z.
        job_type (str): Job type to return worker metrics for. Example: fetch-customer-data.
    """

    from_: datetime.datetime
    to: datetime.datetime
    job_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        job_type = self.job_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
                "jobType": job_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        job_type = d.pop("jobType")

        job_worker_statistics_filter = cls(
            from_=from_,
            to=to,
            job_type=job_type,
        )

        job_worker_statistics_filter.additional_properties = d
        return job_worker_statistics_filter

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
