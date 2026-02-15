from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
T = TypeVar("T", bound="UserTaskAssignmentRequest")
@_attrs_define
class UserTaskAssignmentRequest:
    assignee: str | Unset = UNSET
    allow_override: bool | None | Unset = UNSET
    action: None | str | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
