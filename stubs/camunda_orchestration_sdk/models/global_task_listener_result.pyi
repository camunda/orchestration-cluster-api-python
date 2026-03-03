from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.global_listener_source_enum import GlobalListenerSourceEnum
from ..models.global_task_listener_event_type_enum import GlobalTaskListenerEventTypeEnum
T = TypeVar("T", bound="GlobalTaskListenerResult")
@_attrs_define
class GlobalTaskListenerResult:
    id: str
    source: GlobalListenerSourceEnum
    event_types: list[GlobalTaskListenerEventTypeEnum]
    type_: str
    retries: int
    after_non_global: bool
    priority: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
