from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_changeset import JobChangeset


T = TypeVar("T", bound="JobUpdateRequest")


@_attrs_define
class JobUpdateRequest:
    """
    Attributes:
        changeset (JobChangeset): JSON object with changed job attribute values. The job cannot be completed or failed
            with this endpoint, use the complete job or fail job endpoints instead.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
    """

    changeset: JobChangeset
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        changeset = self.changeset.to_dict()

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "changeset": changeset,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_changeset import JobChangeset

        d = dict(src_dict)
        changeset = JobChangeset.from_dict(d.pop("changeset"))

        operation_reference = d.pop("operationReference", UNSET)

        job_update_request = cls(
            changeset=changeset,
            operation_reference=operation_reference,
        )

        return job_update_request
