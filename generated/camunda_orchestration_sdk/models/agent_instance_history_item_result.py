from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    AgentHistoryItemKey,
    AgentInstanceKey,
    ElementInstanceKey,
    JobKey,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_history_item_result_commit_status import (
    AgentInstanceHistoryItemResultCommitStatus,
)
from ..models.agent_instance_history_item_result_role import (
    AgentInstanceHistoryItemResultRole,
)

if TYPE_CHECKING:
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
    """A single conversation history item belonging to an agent instance.

    Attributes:
        history_item_key (str): The unique key for this history item. Stable and sortable by creation order. Example:
            6755399441055744.
        agent_instance_key (str): The key of the agent instance this item belongs to. Example: 4503599627370496.
        element_instance_key (str): The key of the AI Agent Task or ad-hoc sub-process element instance under which this
            item was produced. Example: 2251799813686789.
        job_key (str): The key of the job activation during which this item was produced. Example: 2251799813653498.
        job_lease (str): The lease token of the activation that produced this item.
        iteration (int | None): The sequential iteration number this item belongs to. Null if not provided by the
            connector. Example: 1.
        role (AgentInstanceHistoryItemResultRole): The role of this history item in the conversation.
        content (list[DocumentContent | ObjectContent | TextContent]): The content blocks of this history item.
        tool_calls (list[AgentInstanceToolCall]): Tool calls for this item. Empty for USER items and ASSISTANT items
            with no tool dispatches.
            ASSISTANT items: dispatched tool calls with arguments populated.
            TOOL_RESULT items: single-entry array referencing the originating tool call (arguments null).
        metrics (AgentInstanceHistoryItemRequestMetrics | None): Per-call token and latency metrics. Present on
            ASSISTANT items only.
        commit_status (AgentInstanceHistoryItemResultCommitStatus): The commit status of this history item.
        produced_at (datetime.datetime): The connector-side timestamp of when this message was produced.
    """

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

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance_history_item_request_metrics import (
            AgentInstanceHistoryItemRequestMetrics,
        )
        from ..models.document_content import DocumentContent
        from ..models.text_content import TextContent

        history_item_key = self.history_item_key

        agent_instance_key = self.agent_instance_key

        element_instance_key = self.element_instance_key

        job_key = self.job_key

        job_lease = self.job_lease

        iteration: int | None
        iteration = self.iteration

        role = self.role.value

        content: list[dict[str, Any]] = []
        for content_item_data in self.content:
            content_item: dict[str, Any]
            if isinstance(content_item_data, TextContent):
                content_item = content_item_data.to_dict()
            elif isinstance(content_item_data, DocumentContent):
                content_item = content_item_data.to_dict()
            else:
                content_item = content_item_data.to_dict()

            content.append(content_item)

        tool_calls: list[dict[str, Any]] = []
        for tool_calls_item_data in self.tool_calls:
            tool_calls_item = tool_calls_item_data.to_dict()
            tool_calls.append(tool_calls_item)

        metrics: dict[str, Any] | None
        if isinstance(self.metrics, AgentInstanceHistoryItemRequestMetrics):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        commit_status = self.commit_status.value

        produced_at = self.produced_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "historyItemKey": history_item_key,
                "agentInstanceKey": agent_instance_key,
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
                "jobLease": job_lease,
                "iteration": iteration,
                "role": role,
                "content": content,
                "toolCalls": tool_calls,
                "metrics": metrics,
                "commitStatus": commit_status,
                "producedAt": produced_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_history_item_request_metrics import (
            AgentInstanceHistoryItemRequestMetrics,
        )
        from ..models.agent_instance_tool_call import AgentInstanceToolCall
        from ..models.document_content import DocumentContent
        from ..models.object_content import ObjectContent
        from ..models.text_content import TextContent

        d = dict(src_dict)
        history_item_key = AgentHistoryItemKey(d.pop("historyItemKey"))

        agent_instance_key = AgentInstanceKey(d.pop("agentInstanceKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        job_key = JobKey(d.pop("jobKey"))

        job_lease = d.pop("jobLease")

        def _parse_iteration(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        iteration = _parse_iteration(d.pop("iteration"))

        role = AgentInstanceHistoryItemResultRole(d.pop("role"))

        content: list[DocumentContent | ObjectContent | TextContent] = []
        _content = d.pop("content")
        for content_item_data in _content:

            def _parse_content_item(
                data: object,
            ) -> DocumentContent | ObjectContent | TextContent:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_agent_instance_message_content_type_0 = (
                        TextContent.from_dict(data)
                    )

                    return componentsschemas_agent_instance_message_content_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_agent_instance_message_content_type_1 = (
                        DocumentContent.from_dict(data)
                    )

                    return componentsschemas_agent_instance_message_content_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_agent_instance_message_content_type_2 = (
                    ObjectContent.from_dict(data)
                )

                return componentsschemas_agent_instance_message_content_type_2

            content_item = _parse_content_item(content_item_data)

            content.append(content_item)

        tool_calls: list[AgentInstanceToolCall] = []
        _tool_calls = d.pop("toolCalls")
        for tool_calls_item_data in _tool_calls:
            tool_calls_item = AgentInstanceToolCall.from_dict(tool_calls_item_data)

            tool_calls.append(tool_calls_item)

        def _parse_metrics(
            data: object,
        ) -> AgentInstanceHistoryItemRequestMetrics | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_agent_instance_history_item_request_metrics_type_0 = (
                    AgentInstanceHistoryItemRequestMetrics.from_dict(data)
                )

                return (
                    componentsschemas_agent_instance_history_item_request_metrics_type_0
                )
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentInstanceHistoryItemRequestMetrics | None, data)

        metrics = _parse_metrics(d.pop("metrics"))

        commit_status = AgentInstanceHistoryItemResultCommitStatus(
            d.pop("commitStatus")
        )

        produced_at = isoparse(d.pop("producedAt"))

        agent_instance_history_item_result = cls(
            history_item_key=history_item_key,
            agent_instance_key=agent_instance_key,
            element_instance_key=element_instance_key,
            job_key=job_key,
            job_lease=job_lease,
            iteration=iteration,
            role=role,
            content=content,
            tool_calls=tool_calls,
            metrics=metrics,
            commit_status=commit_status,
            produced_at=produced_at,
        )

        agent_instance_history_item_result.additional_properties = d
        return agent_instance_history_item_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
