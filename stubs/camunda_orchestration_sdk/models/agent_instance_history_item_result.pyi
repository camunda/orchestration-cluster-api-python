from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    AgentHistoryItemKey,
    AgentInstanceKey,
    ElementInstanceKey,
    JobKey,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.agent_instance_history_item_result_commit_status import (
    AgentInstanceHistoryItemResultCommitStatus,
)
from ..models.agent_instance_history_item_result_role import (
    AgentInstanceHistoryItemResultRole,
)
from ..models.agent_instance_history_item_request_metrics import (
    AgentInstanceHistoryItemRequestMetrics,
)
from ..models.agent_instance_tool_call import AgentInstanceToolCall
from ..models.document_content import DocumentContent
from ..models.object_content import ObjectContent
from ..models.text_content import TextContent

T = TypeVar("T", bound="AgentInstanceHistoryItemResult")

@_attrs_define
class AgentInstanceHistoryItemResult:
    history_item_key: AgentHistoryItemKey
    agent_instance_key: AgentInstanceKey
    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    iteration: int | None
    role: AgentInstanceHistoryItemResultRole
    content: list[DocumentContent | ObjectContent | TextContent]
    tool_calls: list[AgentInstanceToolCall]
    metrics: AgentInstanceHistoryItemRequestMetrics | None
    commit_status: AgentInstanceHistoryItemResultCommitStatus
    produced_at: datetime.datetime
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
