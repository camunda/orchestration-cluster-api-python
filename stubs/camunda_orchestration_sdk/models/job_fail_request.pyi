from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import JobLeaseToken
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.job_fail_request_variables import JobFailRequestVariables

T = TypeVar("T", bound="JobFailRequest")

@_attrs_define
class JobFailRequest:
    retries: int | Unset = UNSET
    error_message: str | Unset = UNSET
    retry_back_off: int | Unset = UNSET
    variables: JobFailRequestVariables | Unset = UNSET
    job_lease_token: None | JobLeaseToken | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
