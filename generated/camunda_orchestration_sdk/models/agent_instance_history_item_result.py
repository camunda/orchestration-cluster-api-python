from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    AgentHistoryItemKey,
    AgentInstanceKey,
    ElementInstanceKey,
    HistoryItemId,
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
    from ..models.agent_instance_history_item_result_limits import (
        AgentInstanceHistoryItemResultLimits,
    )
    from ..models.agent_instance_history_item_result_metrics import (
        AgentInstanceHistoryItemResultMetrics,
    )
    from ..models.agent_instance_tool_call import AgentInstanceToolCall
    from ..models.agent_tool import AgentTool
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
        history_item_id (str): The client-supplied identifier this item was created with. Empty for items that don't
            carry one. Not unique: a job can be re-activated under a superseded lease any number
            of times before it completes, so one historyItemId can have zero or more DISCARDED
            records and at most one COMMITTED record, since only historyItemKey is guaranteed
            unique. Filter by commitStatus rather than assuming one record per historyItemId.
             Example: item-1.
        agent_instance_key (str): The key of the agent instance this item belongs to. Example: 4503599627370496.
        element_instance_key (str): The key of the AI Agent Task or ad-hoc sub-process element instance under which this
            item was produced. Example: 2251799813686789.
        job_key (str): The key of the job activation during which this item was produced. Example: 2251799813653498.
        job_lease (str): The lease token of the activation that produced this item.
        loop_iteration (int): The loop iteration this item belongs to. Example: 1.
        role (AgentInstanceHistoryItemResultRole): The role of this history item in the conversation.
        content (list[DocumentContent | ObjectContent | TextContent]): The content blocks of this history item.
        tool_calls (list[AgentInstanceToolCall]): Tool calls for this item. Empty for USER items and ASSISTANT items
            with no tool dispatches.
            ASSISTANT items: dispatched tool calls.
            TOOL_RESULT items: single-entry array referencing the originating tool call.
        metrics (AgentInstanceHistoryItemResultMetrics | None): Per-call token and latency metrics. Null when metrics
            were not provided at creation time.
        commit_status (AgentInstanceHistoryItemResultCommitStatus): The commit status of this history item.
        produced_at (datetime.datetime): The agent-side timestamp of when this message was produced.
        tools (list[AgentTool]): The complete list of tools available to the agent as of this entry. CONFIGURATION
            items only; empty for other roles.
        model (None | str): The LLM model identifier as of this entry. CONFIGURATION items only; null for other
            roles.
        provider (None | str): The LLM provider as of this entry. CONFIGURATION items only; null for other roles.
        limits (AgentInstanceHistoryItemResultLimits): The operational limits as of this entry. CONFIGURATION items
            only; -1 on any field
            means "no limit configured" for other roles.
        system_prompt (list[DocumentContent | ObjectContent | TextContent]): The system prompt, as content blocks, as of
            this entry. CONFIGURATION items only;
            empty for other roles.
    """

    history_item_key: AgentHistoryItemKey
    history_item_id: HistoryItemId
    agent_instance_key: AgentInstanceKey
    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    loop_iteration: int
    role: AgentInstanceHistoryItemResultRole
    content: list[DocumentContent | ObjectContent | TextContent]
    tool_calls: list[AgentInstanceToolCall]
    metrics: AgentInstanceHistoryItemResultMetrics | None
    commit_status: AgentInstanceHistoryItemResultCommitStatus
    produced_at: datetime.datetime
    tools: list[AgentTool]
    model: None | str
    provider: None | str
    limits: AgentInstanceHistoryItemResultLimits
    system_prompt: list[DocumentContent | ObjectContent | TextContent]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance_history_item_result_metrics import (
            AgentInstanceHistoryItemResultMetrics,
        )
        from ..models.document_content import DocumentContent
        from ..models.text_content import TextContent

        history_item_key = self.history_item_key

        history_item_id = self.history_item_id

        agent_instance_key = self.agent_instance_key

        element_instance_key = self.element_instance_key

        job_key = self.job_key

        job_lease = self.job_lease

        loop_iteration = self.loop_iteration

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
        if isinstance(self.metrics, AgentInstanceHistoryItemResultMetrics):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        commit_status = self.commit_status.value

        produced_at = self.produced_at.isoformat()

        tools: list[dict[str, Any]] = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        model: None | str
        model = self.model

        provider: None | str
        provider = self.provider

        limits = self.limits.to_dict()

        system_prompt: list[dict[str, Any]] = []
        for system_prompt_item_data in self.system_prompt:
            system_prompt_item: dict[str, Any]
            if isinstance(system_prompt_item_data, TextContent):
                system_prompt_item = system_prompt_item_data.to_dict()
            elif isinstance(system_prompt_item_data, DocumentContent):
                system_prompt_item = system_prompt_item_data.to_dict()
            else:
                system_prompt_item = system_prompt_item_data.to_dict()

            system_prompt.append(system_prompt_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "historyItemKey": history_item_key,
                "historyItemId": history_item_id,
                "agentInstanceKey": agent_instance_key,
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
                "jobLease": job_lease,
                "loopIteration": loop_iteration,
                "role": role,
                "content": content,
                "toolCalls": tool_calls,
                "metrics": metrics,
                "commitStatus": commit_status,
                "producedAt": produced_at,
                "tools": tools,
                "model": model,
                "provider": provider,
                "limits": limits,
                "systemPrompt": system_prompt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_history_item_result_limits import (
            AgentInstanceHistoryItemResultLimits,
        )
        from ..models.agent_instance_history_item_result_metrics import (
            AgentInstanceHistoryItemResultMetrics,
        )
        from ..models.agent_instance_tool_call import AgentInstanceToolCall
        from ..models.agent_tool import AgentTool
        from ..models.document_content import DocumentContent
        from ..models.object_content import ObjectContent
        from ..models.text_content import TextContent

        d = dict(src_dict)
        history_item_key = AgentHistoryItemKey(d.pop("historyItemKey"))

        history_item_id = HistoryItemId(d.pop("historyItemId"))

        agent_instance_key = AgentInstanceKey(d.pop("agentInstanceKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        job_key = JobKey(d.pop("jobKey"))

        job_lease = d.pop("jobLease")

        loop_iteration = d.pop("loopIteration")

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
        ) -> AgentInstanceHistoryItemResultMetrics | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_agent_instance_history_item_result_metrics_type_0 = (
                    AgentInstanceHistoryItemResultMetrics.from_dict(data)
                )

                return (
                    componentsschemas_agent_instance_history_item_result_metrics_type_0
                )
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentInstanceHistoryItemResultMetrics | None, data)

        metrics = _parse_metrics(d.pop("metrics"))

        commit_status = AgentInstanceHistoryItemResultCommitStatus(
            d.pop("commitStatus")
        )

        produced_at = isoparse(d.pop("producedAt"))

        tools: list[AgentTool] = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = AgentTool.from_dict(tools_item_data)

            tools.append(tools_item)

        def _parse_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        model = _parse_model(d.pop("model"))

        def _parse_provider(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        provider = _parse_provider(d.pop("provider"))

        limits = AgentInstanceHistoryItemResultLimits.from_dict(d.pop("limits"))

        system_prompt: list[DocumentContent | ObjectContent | TextContent] = []
        _system_prompt = d.pop("systemPrompt")
        for system_prompt_item_data in _system_prompt:

            def _parse_system_prompt_item(
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

            system_prompt_item = _parse_system_prompt_item(system_prompt_item_data)

            system_prompt.append(system_prompt_item)

        agent_instance_history_item_result = cls(
            history_item_key=history_item_key,
            history_item_id=history_item_id,
            agent_instance_key=agent_instance_key,
            element_instance_key=element_instance_key,
            job_key=job_key,
            job_lease=job_lease,
            loop_iteration=loop_iteration,
            role=role,
            content=content,
            tool_calls=tool_calls,
            metrics=metrics,
            commit_status=commit_status,
            produced_at=produced_at,
            tools=tools,
            model=model,
            provider=provider,
            limits=limits,
            system_prompt=system_prompt,
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
