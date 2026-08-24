from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.agent_instance_history_item_role import AgentInstanceHistoryItemRole
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.agent_instance_history_item_limits import AgentInstanceHistoryItemLimits
from ..models.agent_instance_history_item_metrics_1 import (
    AgentInstanceHistoryItemMetrics1,
)
from ..models.agent_instance_tool_call import AgentInstanceToolCall
from ..models.agent_tool import AgentTool
from ..models.document_content import DocumentContent
from ..models.object_content import ObjectContent
from ..models.text_content import TextContent

T = TypeVar("T", bound="AgentInstanceHistoryItem")

@_attrs_define
class AgentInstanceHistoryItem:
    history_item_id: str
    loop_iteration: int
    role: AgentInstanceHistoryItemRole
    content: list[DocumentContent | ObjectContent | TextContent]
    produced_at: datetime.datetime
    tool_calls: list[AgentInstanceToolCall] | None | Unset = UNSET
    metrics: AgentInstanceHistoryItemMetrics1 | None | Unset = UNSET
    tools: list[AgentTool] | None | Unset = UNSET
    model: str | Unset = UNSET
    provider: str | Unset = UNSET
    limits: AgentInstanceHistoryItemLimits | Unset = UNSET
    system_prompt: (
        list[DocumentContent | ObjectContent | TextContent] | None | Unset
    ) = UNSET
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
