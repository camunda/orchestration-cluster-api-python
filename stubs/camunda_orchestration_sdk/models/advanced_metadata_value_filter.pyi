from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedMetadataValueFilter")

@_attrs_define
class AdvancedMetadataValueFilter:
    eq: float | str | Unset = UNSET
    neq: float | str | Unset = UNSET
    exists: bool | Unset = UNSET
    gt: float | Unset = UNSET
    gte: float | Unset = UNSET
    lt: float | Unset = UNSET
    lte: float | Unset = UNSET
    in_: list[float | str] | Unset = UNSET
    like: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
