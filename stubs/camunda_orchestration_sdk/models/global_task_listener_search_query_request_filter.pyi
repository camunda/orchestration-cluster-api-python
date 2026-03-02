from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.global_listener_source_exact_match import GlobalListenerSourceExactMatch
from ..models.global_task_listener_event_type_exact_match import GlobalTaskListenerEventTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_global_listener_source_filter import AdvancedGlobalListenerSourceFilter
from ..models.advanced_global_task_listener_event_type_filter import AdvancedGlobalTaskListenerEventTypeFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_string_filter import AdvancedStringFilter
T = TypeVar("T", bound="GlobalTaskListenerSearchQueryRequestFilter")
@_attrs_define
class GlobalTaskListenerSearchQueryRequestFilter:
    id: AdvancedStringFilter | str | Unset = UNSET
    type_: AdvancedStringFilter | str | Unset = UNSET
    retries: AdvancedIntegerFilter | int | Unset = UNSET
    event_types: (
            list[
                AdvancedGlobalTaskListenerEventTypeFilter
                | GlobalTaskListenerEventTypeExactMatch
            ]
            | Unset
        ) = UNSET
    after_non_global: bool | Unset = UNSET
    priority: AdvancedIntegerFilter | int | Unset = UNSET
    source: (
            AdvancedGlobalListenerSourceFilter | GlobalListenerSourceExactMatch | Unset
        ) = UNSET
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
