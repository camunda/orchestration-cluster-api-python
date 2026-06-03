from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.user_task_completion_request_variables import UserTaskCompletionRequestVariables
T = TypeVar("T", bound="UserTaskCompletionRequest")
@_attrs_define
class UserTaskCompletionRequest:
    variables: None | Unset | UserTaskCompletionRequestVariables = UNSET
    action: None | str | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
