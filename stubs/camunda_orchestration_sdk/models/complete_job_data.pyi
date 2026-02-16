from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.job_completion_request_variables import JobCompletionRequestVariables
from ..models.job_result_user_task_type_0 import JobResultUserTaskType0
from ..models.result_object_type_0 import ResultObjectType0

T = TypeVar("T", bound="CompleteJobData")

@_attrs_define
class CompleteJobData:
    variables: JobCompletionRequestVariables | None | Unset = UNSET
    result: JobResultUserTaskType0 | None | ResultObjectType0 | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
