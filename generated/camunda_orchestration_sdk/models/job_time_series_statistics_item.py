from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.status_metric import StatusMetric


T = TypeVar("T", bound="JobTimeSeriesStatisticsItem")


@_attrs_define
class JobTimeSeriesStatisticsItem:
    """Aggregated job metrics for a single time bucket.

    Attributes:
        time (datetime.datetime): ISO 8601 timestamp representing the start of this time bucket. Example:
            2024-07-29T15:51:00.000Z.
        created (StatusMetric): Metric for a single job status.
        completed (StatusMetric): Metric for a single job status.
        failed (StatusMetric): Metric for a single job status.
    """

    time: datetime.datetime
    created: StatusMetric
    completed: StatusMetric
    failed: StatusMetric
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        time = self.time.isoformat()

        created = self.created.to_dict()

        completed = self.completed.to_dict()

        failed = self.failed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "time": time,
                "created": created,
                "completed": completed,
                "failed": failed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status_metric import StatusMetric

        d = dict(src_dict)
        time = isoparse(d.pop("time"))

        created = StatusMetric.from_dict(d.pop("created"))

        completed = StatusMetric.from_dict(d.pop("completed"))

        failed = StatusMetric.from_dict(d.pop("failed"))

        job_time_series_statistics_item = cls(
            time=time,
            created=created,
            completed=completed,
            failed=failed,
        )

        job_time_series_statistics_item.additional_properties = d
        return job_time_series_statistics_item

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
