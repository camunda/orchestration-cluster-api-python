from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
        lease_token (None | str | Unset): The token identifying a leased job's activation, obtained from
            `ActivatedJobResult.leaseToken`.
            For a leased job, a supplied token is validated to prove the command comes from the worker that holds the
            current lease; a command carrying a stale token is rejected, fencing the job against a superseded activation
            (for example, after the job timed out or failed and was re-activated by another worker).
            An update without a token always applies to support operator and bulk updates of leased jobs. Note that this is
            different from lifecycle requests like complete, fail, and throw-error that always require a token for leased
            jobs.
            A job that was activated without a lease requires no token.
    """

    changeset: JobChangeset
    operation_reference: int | Unset = UNSET
    lease_token: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        changeset = self.changeset.to_dict()

        operation_reference = self.operation_reference

        lease_token: None | str | Unset
        if isinstance(self.lease_token, Unset):
            lease_token = UNSET
        else:
            lease_token = self.lease_token

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "changeset": changeset,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference
        if lease_token is not UNSET:
            field_dict["leaseToken"] = lease_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_changeset import JobChangeset

        d = dict(src_dict)
        changeset = JobChangeset.from_dict(d.pop("changeset"))

        operation_reference = d.pop("operationReference", UNSET)

        def _parse_lease_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lease_token = _parse_lease_token(d.pop("leaseToken", UNSET))

        job_update_request = cls(
            changeset=changeset,
            operation_reference=operation_reference,
            lease_token=lease_token,
        )

        return job_update_request
