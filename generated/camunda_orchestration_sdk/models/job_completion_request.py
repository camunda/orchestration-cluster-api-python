from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_completion_request_variables import JobCompletionRequestVariables
    from ..models.job_result_ad_hoc_sub_process import (
        JobResultAdHocSubProcess,
    )
    from ..models.job_result_user_task import JobResultUserTask


T = TypeVar("T", bound="JobCompletionRequest")


@_attrs_define
class JobCompletionRequest:
    """
    Attributes:
        variables (JobCompletionRequestVariables | None | Unset): The variables to complete the job with.
        result (JobResultAdHocSubProcess | JobResultUserTask | None | Unset): The result of the completed job
            as determined by the worker.
        lease_token (None | str | Unset): The token identifying a leased job's activation, obtained from
            `ActivatedJobResult.leaseToken`.
            For a leased job, the matching token must be supplied to prove the command comes from the worker that holds the
            current lease; a command with no token is rejected. A command carrying a stale token is likewise rejected,
            fencing the job against a superseded activation (for example, after the job timed out or failed and was re-
            activated by another worker).
            A job that was activated without a lease requires no token.
    """

    variables: JobCompletionRequestVariables | None | Unset = UNSET
    result: JobResultAdHocSubProcess | JobResultUserTask | None | Unset = UNSET
    lease_token: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_completion_request_variables import (
            JobCompletionRequestVariables,
        )
        from ..models.job_result_ad_hoc_sub_process import (
            JobResultAdHocSubProcess,
        )
        from ..models.job_result_user_task import JobResultUserTask

        variables: dict[str, Any] | None | Unset
        if isinstance(self.variables, Unset):
            variables = UNSET
        elif isinstance(self.variables, JobCompletionRequestVariables):
            variables = self.variables.to_dict()
        else:
            variables = self.variables

        result: dict[str, Any] | None | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, JobResultUserTask):
            result = self.result.to_dict()
        elif isinstance(self.result, JobResultAdHocSubProcess):
            result = self.result.to_dict()
        else:
            result = self.result

        lease_token: None | str | Unset
        if isinstance(self.lease_token, Unset):
            lease_token = UNSET
        else:
            lease_token = self.lease_token

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if variables is not UNSET:
            field_dict["variables"] = variables
        if result is not UNSET:
            field_dict["result"] = result
        if lease_token is not UNSET:
            field_dict["leaseToken"] = lease_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_completion_request_variables import (
            JobCompletionRequestVariables,
        )
        from ..models.job_result_ad_hoc_sub_process import (
            JobResultAdHocSubProcess,
        )
        from ..models.job_result_user_task import JobResultUserTask

        d = dict(src_dict)

        def _parse_variables(
            data: object,
        ) -> JobCompletionRequestVariables | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_job_completion_request_variables_type_0 = (
                    JobCompletionRequestVariables.from_dict(data)
                )

                return componentsschemas_job_completion_request_variables_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobCompletionRequestVariables | None | Unset, data)

        variables = _parse_variables(d.pop("variables", UNSET))

        def _parse_result(
            data: object,
        ) -> JobResultAdHocSubProcess | JobResultUserTask | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_job_result_user_task_type_0 = (
                    JobResultUserTask.from_dict(data)
                )

                return componentsschemas_job_result_user_task_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_job_result_ad_hoc_sub_process_type_0 = (
                    JobResultAdHocSubProcess.from_dict(data)
                )

                return componentsschemas_job_result_ad_hoc_sub_process_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                JobResultAdHocSubProcess | JobResultUserTask | None | Unset,
                data,
            )

        result = _parse_result(d.pop("result", UNSET))

        def _parse_lease_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lease_token = _parse_lease_token(d.pop("leaseToken", UNSET))

        job_completion_request = cls(
            variables=variables,
            result=result,
            lease_token=lease_token,
        )

        return job_completion_request
