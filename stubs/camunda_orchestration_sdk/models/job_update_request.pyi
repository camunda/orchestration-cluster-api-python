from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import JobLeaseToken
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.job_changeset import JobChangeset

T = TypeVar("T", bound="JobUpdateRequest")

@_attrs_define
class JobUpdateRequest:
    changeset: JobChangeset
    operation_reference: int | Unset = UNSET
    job_lease_token: None | JobLeaseToken | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
