from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.secret_list_request_filter import SecretListRequestFilter

T = TypeVar("T", bound="SecretListRequest")

@_attrs_define
class SecretListRequest:
    filter_: SecretListRequestFilter | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
