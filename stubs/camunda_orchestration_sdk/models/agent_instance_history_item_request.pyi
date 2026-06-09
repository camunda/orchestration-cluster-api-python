from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.agent_instance_history_item_request_role import (
    AgentInstanceHistoryItemRequestRole,
)
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.agent_instance_history_item_request_metrics import (
    AgentInstanceHistoryItemRequestMetrics,
)
from ..models.agent_instance_tool_call import AgentInstanceToolCall
from ..models.document_content import DocumentContent
from ..models.object_content import ObjectContent
from ..models.text_content import TextContent

T = TypeVar("T", bound="AgentInstanceHistoryItemRequest")

@_attrs_define
class AgentInstanceHistoryItemRequest:
    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    role: AgentInstanceHistoryItemRequestRole
    content: list[DocumentContent | ObjectContent | TextContent]
    produced_at: datetime.datetime
    iteration: int | None | Unset = UNSET
    tool_calls: list[AgentInstanceToolCall] | None | Unset = UNSET
    metrics: AgentInstanceHistoryItemRequestMetrics | None | Unset = UNSET
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
