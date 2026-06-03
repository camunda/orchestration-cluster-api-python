from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import Username
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
T = TypeVar("T", bound="UserRequest")
@_attrs_define
class UserRequest:
    password: str
    username: Username
    name: str | Unset = UNSET
    email: str | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
