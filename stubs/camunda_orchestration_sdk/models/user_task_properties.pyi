from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import FormKey, UserTaskKey
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="UserTaskProperties")
@_attrs_define
class UserTaskProperties:
    candidate_groups: list[str]
    candidate_users: list[str]
    changed_attributes: list[str]
    action: str | Unset = UNSET
    assignee: None | str | Unset = UNSET
    due_date: None | str | Unset = UNSET
    follow_up_date: None | str | Unset = UNSET
    form_key: FormKey | Unset = UNSET
    priority: int | None | Unset = UNSET
    user_task_key: None | UserTaskKey | Unset = UNSET
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
