from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.job_error_request_variables import JobErrorRequestVariables
T = TypeVar("T", bound="JobErrorRequest")
@_attrs_define
class JobErrorRequest:
    error_code: str
    error_message: None | str | Unset = UNSET
    variables: JobErrorRequestVariables | None | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
