from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_batch_update_request_changeset import (
        JobBatchUpdateRequestChangeset,
    )
    from ..models.job_batch_update_request_filter import JobBatchUpdateRequestFilter


T = TypeVar("T", bound="JobBatchUpdateRequest")


@_attrs_define
class JobBatchUpdateRequest:
    """The filter and changeset for a batch job update operation. The filter defines which jobs are updated; the changeset
    defines what to update. At least one changeset field must be non-null.

        Attributes:
            filter_ (JobBatchUpdateRequestFilter): The job filter. At least one dimension must be set.
            changeset (JobBatchUpdateRequestChangeset): The fields to update. At least one field must be non-null.
            operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
                from this operation.
                Must be > 0 if provided.
    """

    filter_: JobBatchUpdateRequestFilter
    changeset: JobBatchUpdateRequestChangeset
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        changeset = self.changeset.to_dict()

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "filter": filter_,
                "changeset": changeset,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_batch_update_request_changeset import (
            JobBatchUpdateRequestChangeset,
        )
        from ..models.job_batch_update_request_filter import JobBatchUpdateRequestFilter

        d = dict(src_dict)
        filter_ = JobBatchUpdateRequestFilter.from_dict(d.pop("filter"))

        changeset = JobBatchUpdateRequestChangeset.from_dict(d.pop("changeset"))

        operation_reference = d.pop("operationReference", UNSET)

        job_batch_update_request = cls(
            filter_=filter_,
            changeset=changeset,
            operation_reference=operation_reference,
        )

        return job_batch_update_request
