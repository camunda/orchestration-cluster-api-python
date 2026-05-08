from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_metric import StatusMetric


T = TypeVar("T", bound="JobTypeStatisticsItem")


@_attrs_define
class JobTypeStatisticsItem:
    """Statistics for a single job type.

    Attributes:
        job_type (str): The job type identifier. Example: fetch-customer-data.
        created (StatusMetric): Metric for a single job status.
        completed (StatusMetric): Metric for a single job status.
        failed (StatusMetric): Metric for a single job status.
        workers (int): Number of distinct workers observed for this job type. Example: 5.
    """

    job_type: str
    created: StatusMetric
    completed: StatusMetric
    failed: StatusMetric
    workers: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        job_type = self.job_type

        created = self.created.to_dict()

        completed = self.completed.to_dict()

        failed = self.failed.to_dict()

        workers = self.workers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobType": job_type,
                "created": created,
                "completed": completed,
                "failed": failed,
                "workers": workers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status_metric import StatusMetric

        d = dict(src_dict)
        job_type = d.pop("jobType")

        created = StatusMetric.from_dict(d.pop("created"))

        completed = StatusMetric.from_dict(d.pop("completed"))

        failed = StatusMetric.from_dict(d.pop("failed"))

        workers = d.pop("workers")

        job_type_statistics_item = cls(
            job_type=job_type,
            created=created,
            completed=completed,
            failed=failed,
            workers=workers,
        )

        job_type_statistics_item.additional_properties = d
        return job_type_statistics_item

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
