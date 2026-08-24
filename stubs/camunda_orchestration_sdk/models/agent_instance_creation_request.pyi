from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.agent_instance_history_item import AgentInstanceHistoryItem

T = TypeVar("T", bound="AgentInstanceCreationRequest")

@_attrs_define
class AgentInstanceCreationRequest:
    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    history: list[AgentInstanceHistoryItem]
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
