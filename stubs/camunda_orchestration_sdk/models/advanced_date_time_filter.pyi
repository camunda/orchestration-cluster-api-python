from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedDateTimeFilter")

@_attrs_define
class AdvancedDateTimeFilter:
    eq: datetime.datetime | Unset = UNSET
    neq: datetime.datetime | Unset = UNSET
    exists: bool | Unset = UNSET
    gt: datetime.datetime | Unset = UNSET
    gte: datetime.datetime | Unset = UNSET
    lt: datetime.datetime | Unset = UNSET
    lte: datetime.datetime | Unset = UNSET
    in_: list[datetime.datetime] | Unset = UNSET
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
