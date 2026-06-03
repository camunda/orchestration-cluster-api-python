from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import JobKey

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.job_wait_state_details_job_kind import JobWaitStateDetailsJobKind
from ..models.job_wait_state_details_listener_event_type import (
    JobWaitStateDetailsListenerEventType,
)

T = TypeVar("T", bound="JobWaitStateDetails")


@_attrs_define
class JobWaitStateDetails:
    """
    Attributes:
        job_key (str): The key of the job. Example: 2251799813653498.
        job_type (str): The job type (worker subscription identifier).
        job_kind (JobWaitStateDetailsJobKind): The kind of job. Example: BPMN_ELEMENT.
        listener_event_type (JobWaitStateDetailsListenerEventType): The listener event type of the job (only set for
            execution listener and task listener jobs). Example: UNSPECIFIED.
        retries (int | None): The number of retries remaining for the job.
    """

    job_key: JobKey
    job_type: str
    job_kind: JobWaitStateDetailsJobKind
    listener_event_type: JobWaitStateDetailsListenerEventType
    retries: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        job_key = self.job_key

        job_type = self.job_type

        job_kind = self.job_kind.value

        listener_event_type = self.listener_event_type.value

        retries: int | None
        retries = self.retries

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobKey": job_key,
                "jobType": job_type,
                "jobKind": job_kind,
                "listenerEventType": listener_event_type,
                "retries": retries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_key = JobKey(d.pop("jobKey"))

        job_type = d.pop("jobType")

        job_kind = JobWaitStateDetailsJobKind(d.pop("jobKind"))

        listener_event_type = JobWaitStateDetailsListenerEventType(
            d.pop("listenerEventType")
        )

        def _parse_retries(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        retries = _parse_retries(d.pop("retries"))

        job_wait_state_details = cls(
            job_key=job_key,
            job_type=job_type,
            job_kind=job_kind,
            listener_event_type=listener_event_type,
            retries=retries,
        )

        job_wait_state_details.additional_properties = d
        return job_wait_state_details

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
