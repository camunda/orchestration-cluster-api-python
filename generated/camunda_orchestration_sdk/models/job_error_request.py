from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_error_request_variables import JobErrorRequestVariables


T = TypeVar("T", bound="JobErrorRequest")


@_attrs_define
class JobErrorRequest:
    """
    Attributes:
        error_code (str): The error code that will be matched with an error catch event.
        error_message (None | str | Unset): An error message that provides additional context.
        variables (JobErrorRequestVariables | None | Unset): JSON object that will instantiate the variables at the
            local scope of the error catch event that catches the thrown error.
    """

    error_code: str
    error_message: None | str | Unset = UNSET
    variables: JobErrorRequestVariables | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_error_request_variables import JobErrorRequestVariables

        error_code = self.error_code

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        variables: dict[str, Any] | None | Unset
        if isinstance(self.variables, Unset):
            variables = UNSET
        elif isinstance(self.variables, JobErrorRequestVariables):
            variables = self.variables.to_dict()
        else:
            variables = self.variables

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "errorCode": error_code,
            }
        )
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_error_request_variables import JobErrorRequestVariables

        d = dict(src_dict)
        error_code = d.pop("errorCode")

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("errorMessage", UNSET))

        def _parse_variables(data: object) -> JobErrorRequestVariables | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_job_error_request_variables_type_0 = (
                    JobErrorRequestVariables.from_dict(data)
                )

                return componentsschemas_job_error_request_variables_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobErrorRequestVariables | None | Unset, data)

        variables = _parse_variables(d.pop("variables", UNSET))

        job_error_request = cls(
            error_code=error_code,
            error_message=error_message,
            variables=variables,
        )

        return job_error_request
