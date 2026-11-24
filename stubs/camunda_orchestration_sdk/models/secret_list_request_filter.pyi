from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.secret_status_exact_match import SecretStatusExactMatch
from ..types import UNSET, Unset
from ..models.advanced_secret_status_filter import AdvancedSecretStatusFilter

T = TypeVar("T", bound="SecretListRequestFilter")

@_attrs_define
class SecretListRequestFilter:
    status: AdvancedSecretStatusFilter | SecretStatusExactMatch | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
