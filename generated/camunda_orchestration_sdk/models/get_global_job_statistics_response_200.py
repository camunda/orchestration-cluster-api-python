from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_global_job_statistics_response_200_completed import (
        GetGlobalJobStatisticsResponse200Completed,
    )
    from ..models.get_global_job_statistics_response_200_created import (
        GetGlobalJobStatisticsResponse200Created,
    )
    from ..models.get_global_job_statistics_response_200_failed import (
        GetGlobalJobStatisticsResponse200Failed,
    )


T = TypeVar("T", bound="GetGlobalJobStatisticsResponse200")


@_attrs_define
class GetGlobalJobStatisticsResponse200:
    """Global job statistics query result.

    Attributes:
        created (GetGlobalJobStatisticsResponse200Created): Metric for a single job status.
        completed (GetGlobalJobStatisticsResponse200Completed): Metric for a single job status.
        failed (GetGlobalJobStatisticsResponse200Failed): Metric for a single job status.
        is_incomplete (bool): True if some data is missing because internal limits were reached and some metrics were
            not recorded.
    """

    created: GetGlobalJobStatisticsResponse200Created
    completed: GetGlobalJobStatisticsResponse200Completed
    failed: GetGlobalJobStatisticsResponse200Failed
    is_incomplete: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

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
        from ..models.get_global_job_statistics_response_200_completed import (
            GetGlobalJobStatisticsResponse200Completed,
        )
        from ..models.get_global_job_statistics_response_200_created import (
            GetGlobalJobStatisticsResponse200Created,
        )
        from ..models.get_global_job_statistics_response_200_failed import (
            GetGlobalJobStatisticsResponse200Failed,
        )

        d = dict(src_dict)
        created = GetGlobalJobStatisticsResponse200Created.from_dict(d.pop("created"))

        completed = GetGlobalJobStatisticsResponse200Completed.from_dict(
            d.pop("completed")
        )

        failed = GetGlobalJobStatisticsResponse200Failed.from_dict(d.pop("failed"))

        is_incomplete = d.pop("isIncomplete")

        get_global_job_statistics_response_200 = cls(
            created=created,
            completed=completed,
            failed=failed,
            is_incomplete=is_incomplete,
        )

        get_global_job_statistics_response_200.additional_properties = d
        return get_global_job_statistics_response_200

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
