from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.job_completion_request_variables import JobCompletionRequestVariables
from ..models.job_result_ad_hoc_sub_process import JobResultAdHocSubProcess
from ..models.job_result_user_task import JobResultUserTask
T = TypeVar("T", bound="JobCompletionRequest")
@_attrs_define
class JobCompletionRequest:
    variables: JobCompletionRequestVariables | None | Unset = UNSET
    result: JobResultAdHocSubProcess | JobResultUserTask | None | Unset = (
            UNSET
        )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
