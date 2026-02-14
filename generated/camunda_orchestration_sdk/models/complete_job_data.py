from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_completion_request_variables import JobCompletionRequestVariables
    from ..models.job_result_user_task_type_0 import JobResultUserTaskType0
    from ..models.result_object_type_0 import ResultObjectType0


T = TypeVar("T", bound="CompleteJobData")


@_attrs_define
class CompleteJobData:
    """
    Attributes:
        variables (JobCompletionRequestVariables | None | Unset): The variables to complete the job with.
        result (JobResultUserTaskType0 | None | ResultObjectType0 | Unset): The result of the completed job as
            determined by the worker.
    """

    variables: JobCompletionRequestVariables | None | Unset = UNSET
    result: JobResultUserTaskType0 | None | ResultObjectType0 | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_completion_request_variables import (
            JobCompletionRequestVariables,
        )
        from ..models.job_result_user_task_type_0 import JobResultUserTaskType0
        from ..models.result_object_type_0 import ResultObjectType0

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
        elif isinstance(self.result, JobResultUserTaskType0):
            result = self.result.to_dict()
        elif isinstance(self.result, ResultObjectType0):
            result = self.result.to_dict()
        else:
            result = self.result

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if variables is not UNSET:
            field_dict["variables"] = variables
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_completion_request_variables import (
            JobCompletionRequestVariables,
        )
        from ..models.job_result_user_task_type_0 import JobResultUserTaskType0
        from ..models.result_object_type_0 import ResultObjectType0

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
        ) -> JobResultUserTaskType0 | None | ResultObjectType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_job_result_user_task_type_0 = (
                    JobResultUserTaskType0.from_dict(data)
                )

                return componentsschemas_job_result_user_task_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_result_object_type_0 = ResultObjectType0.from_dict(
                    data
                )

                return componentsschemas_result_object_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobResultUserTaskType0 | None | ResultObjectType0 | Unset, data)

        result = _parse_result(d.pop("result", UNSET))

        complete_job_data = cls(
            variables=variables,
            result=result,
        )

        return complete_job_data
