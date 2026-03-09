from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_metric import StatusMetric


T = TypeVar("T", bound="JobWorkerStatisticsItem")


@_attrs_define
class JobWorkerStatisticsItem:
    """Statistics for a single worker within a job type.

    Attributes:
        worker (str): The worker identifier. Example: worker-1.
        created (StatusMetric): Metric for a single job status.
        completed (StatusMetric): Metric for a single job status.
        failed (StatusMetric): Metric for a single job status.
    """

    worker: str
    created: StatusMetric
    completed: StatusMetric
    failed: StatusMetric
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        worker = self.worker

        created = self.created.to_dict()

        completed = self.completed.to_dict()

        failed = self.failed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "worker": worker,
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
        worker = d.pop("worker")

        created = StatusMetric.from_dict(d.pop("created"))

        completed = StatusMetric.from_dict(d.pop("completed"))

        failed = StatusMetric.from_dict(d.pop("failed"))

        job_worker_statistics_item = cls(
            worker=worker,
            created=created,
            completed=completed,
            failed=failed,
        )

        job_worker_statistics_item.additional_properties = d
        return job_worker_statistics_item

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
