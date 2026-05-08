from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.activated_job_result import ActivatedJobResult


T = TypeVar("T", bound="JobActivationResult")


@_attrs_define
class JobActivationResult:
    """The list of activated jobs

    Attributes:
        jobs (list[ActivatedJobResult]): The activated jobs.
    """

    jobs: list[ActivatedJobResult]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        jobs: list[dict[str, Any]] = []
        for jobs_item_data in self.jobs:
            jobs_item = jobs_item_data.to_dict()
            jobs.append(jobs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobs": jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activated_job_result import ActivatedJobResult

        d = dict(src_dict)
        jobs: list[ActivatedJobResult] = []
        _jobs = d.pop("jobs")
        for jobs_item_data in _jobs:
            jobs_item = ActivatedJobResult.from_dict(jobs_item_data)

            jobs.append(jobs_item)

        job_activation_result = cls(
            jobs=jobs,
        )

        job_activation_result.additional_properties = d
        return job_activation_result

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
