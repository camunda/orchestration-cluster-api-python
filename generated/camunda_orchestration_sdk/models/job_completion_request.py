from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import BusinessId

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
        business_id (None | str | Unset): An optional business id to assign to the process instance the job belongs to,
            as part of completing the job, letting a worker set the identifier from work it just performed.
            The business id can only be assigned to a root process instance: if the job belongs to a child process instance
            (one started by a call activity), the completion is rejected. An empty business id is likewise rejected. The
            assignment is single and irreversible and is only accepted while business id uniqueness is disabled. Only
            artifacts created after the assignment carry the business id; already-existing ones are not enriched. Completing
            with a business id that differs from one already assigned rejects the whole completion, leaving the job open;
            re-sending the identical business id is an idempotent no-op.
             Example: order-12345.
    """

    variables: JobCompletionRequestVariables | None | Unset = UNSET
    result: JobResultAdHocSubProcess | JobResultUserTask | None | Unset = UNSET
    lease_token: None | str | Unset = UNSET
    business_id: None | BusinessId | Unset = UNSET

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

        business_id: None | BusinessId | Unset
        if isinstance(self.business_id, Unset):
            business_id = UNSET
        else:
            business_id = self.business_id

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if variables is not UNSET:
            field_dict["variables"] = variables
        if result is not UNSET:
            field_dict["result"] = result
        if lease_token is not UNSET:
            field_dict["leaseToken"] = lease_token
        if business_id is not UNSET:
            field_dict["businessId"] = business_id

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

        def _parse_business_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_business_id = _parse_business_id(d.pop("businessId", UNSET))

        business_id = (
            BusinessId(_raw_business_id)
            if isinstance(_raw_business_id, str)
            else _raw_business_id
        )

        job_completion_request = cls(
            variables=variables,
            result=result,
            lease_token=lease_token,
            business_id=business_id,
        )

        return job_completion_request
