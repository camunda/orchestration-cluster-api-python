from __future__ import annotations

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
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
