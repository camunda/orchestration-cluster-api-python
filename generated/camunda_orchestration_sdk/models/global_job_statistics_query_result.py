from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.status_metric import StatusMetric


T = TypeVar("T", bound="GlobalJobStatisticsQueryResult")


@_attrs_define
class GlobalJobStatisticsQueryResult:
    """Global job statistics query result.

    Attributes:
        created (StatusMetric): Metric for a single job status.
        completed (StatusMetric): Metric for a single job status.
        failed (StatusMetric): Metric for a single job status.
        is_incomplete (bool): True if some data is missing because internal limits were reached and some metrics were
            not recorded.
    """

    created: StatusMetric
    completed: StatusMetric
    failed: StatusMetric
    is_incomplete: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        created = self.created.to_dict()

        completed = self.completed.to_dict()

        failed = self.failed.to_dict()

        is_incomplete = self.is_incomplete

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "completed": completed,
                "failed": failed,
                "isIncomplete": is_incomplete,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status_metric import StatusMetric

        d = dict(src_dict)
        created = StatusMetric.from_dict(d.pop("created"))

        completed = StatusMetric.from_dict(d.pop("completed"))

        failed = StatusMetric.from_dict(d.pop("failed"))

        is_incomplete = d.pop("isIncomplete")

        global_job_statistics_query_result = cls(
            created=created,
            completed=completed,
            failed=failed,
            is_incomplete=is_incomplete,
        )

        global_job_statistics_query_result.additional_properties = d
        return global_job_statistics_query_result

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
