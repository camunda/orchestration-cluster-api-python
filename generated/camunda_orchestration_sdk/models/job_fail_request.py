from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import JobLeaseToken

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_fail_request_variables import JobFailRequestVariables


T = TypeVar("T", bound="JobFailRequest")


@_attrs_define
class JobFailRequest:
    """
    Attributes:
        retries (int | Unset): The amount of retries the job should have left Server default: 0.
        error_message (str | Unset): An optional error message describing why the job failed; if not provided, an empty
            string is used.
        retry_back_off (int | Unset): An optional retry back off for the failed job. The job will not be retryable
            before the current time plus the back off time. The default is 0 which means the job is retryable immediately.
            Server default: 0.
        variables (JobFailRequestVariables | Unset): JSON object that will instantiate the variables at the local scope
            of the job's associated task.
        job_lease_token (None | str | Unset): The token identifying a leased job's activation, obtained from
            `ActivatedJobResult.jobLeaseToken`.
            For a leased job, the matching token must be supplied to prove the command comes from the worker that holds the
            current lease; a command with no token is rejected. A command carrying a stale token is likewise rejected,
            fencing the job against a superseded activation (for example, after the job timed out or failed and was re-
            activated by another worker).
            A job that was activated without a lease requires no token.
             Example: 550e8400-e29b-41d4-a716-446655440000.
    """

    retries: int | Unset = UNSET
    error_message: str | Unset = UNSET
    retry_back_off: int | Unset = UNSET
    variables: JobFailRequestVariables | Unset = UNSET
    job_lease_token: None | JobLeaseToken | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        retries = self.retries

        error_message = self.error_message

        retry_back_off = self.retry_back_off

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        job_lease_token: None | JobLeaseToken | Unset
        if isinstance(self.job_lease_token, Unset):
            job_lease_token = UNSET
        else:
            job_lease_token = self.job_lease_token

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if retries is not UNSET:
            field_dict["retries"] = retries
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if retry_back_off is not UNSET:
            field_dict["retryBackOff"] = retry_back_off
        if variables is not UNSET:
            field_dict["variables"] = variables
        if job_lease_token is not UNSET:
            field_dict["jobLeaseToken"] = job_lease_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_fail_request_variables import JobFailRequestVariables

        d = dict(src_dict)
        retries = d.pop("retries", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        retry_back_off = d.pop("retryBackOff", UNSET)

        _variables = d.pop("variables", UNSET)
        variables: JobFailRequestVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = JobFailRequestVariables.from_dict(_variables)

        def _parse_job_lease_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_job_lease_token = _parse_job_lease_token(d.pop("jobLeaseToken", UNSET))

        job_lease_token = (
            JobLeaseToken(_raw_job_lease_token)
            if isinstance(_raw_job_lease_token, str)
            else _raw_job_lease_token
        )

        job_fail_request = cls(
            retries=retries,
            error_message=error_message,
            retry_back_off=retry_back_off,
            variables=variables,
            job_lease_token=job_lease_token,
        )

        return job_fail_request
