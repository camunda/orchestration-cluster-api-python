from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_history_item_role import AgentInstanceHistoryItemRole
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.agent_instance_history_item_limits import (
        AgentInstanceHistoryItemLimits,
    )
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
    """A single history item to append to the agent instance's conversation history,
    submitted as part of the batch on an agent instance update request.

        Attributes:
            history_item_id (str): Caller-assigned identifier used to detect and dedupe retries of the same
                item. For example, when a retried job activation resubmits history items
                it already sent in an earlier attempt, those items are not rejected; they
                are flagged via isDuplicate in the response instead. Must be non-blank.
            loop_iteration (int): The loop iteration this item belongs to. Example: 1.
            role (AgentInstanceHistoryItemRole): The role of this history item in the conversation.
            content (list[DocumentContent | ObjectContent | TextContent]): The content blocks of this history item.
            produced_at (datetime.datetime): The agent-side timestamp of when this message was produced.
            tool_calls (list[AgentInstanceToolCall] | None | Unset): Tool calls associated with this history item.
                For ASSISTANT items: tool calls dispatched by this LLM response.
                For TOOL_RESULT items: single-entry array referencing the originating tool call.
                Omit for USER items.
            metrics (AgentInstanceHistoryItemMetrics1 | None | Unset): Per-call token and latency metrics. Present on
                ASSISTANT items only.
            tools (list[AgentTool] | None | Unset): The complete list of tools available to the agent as of this entry.
                CONFIGURATION
                items only; omit for other roles. Omit to leave the tool list unchanged; send an
                empty array to clear it.
            model (str | Unset): The LLM model identifier as of this entry. CONFIGURATION items only; omit for other
                roles.
            provider (str | Unset): The LLM provider as of this entry. CONFIGURATION items only; omit for other roles.
            limits (AgentInstanceHistoryItemLimits | Unset): The operational limits as of this entry. CONFIGURATION items
                only; omit for other
                roles.
            system_prompt (list[DocumentContent | ObjectContent | TextContent] | None | Unset): The system prompt, as
                content blocks, as of this entry. CONFIGURATION items only;
                omit for other roles. Omit to leave the system prompt unchanged; when present, must
                be non-empty.
    """

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

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance_history_item_metrics_1 import (
            AgentInstanceHistoryItemMetrics1,
        )
        from ..models.document_content import DocumentContent
        from ..models.text_content import TextContent

        history_item_id = self.history_item_id

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

        produced_at = self.produced_at.isoformat()

        tool_calls: list[dict[str, Any]] | None | Unset
        if isinstance(self.tool_calls, Unset):
            tool_calls = UNSET
        elif isinstance(self.tool_calls, list):
            tool_calls = []
            for tool_calls_type_0_item_data in self.tool_calls:
                tool_calls_type_0_item = tool_calls_type_0_item_data.to_dict()
                tool_calls.append(tool_calls_type_0_item)

        else:
            tool_calls = self.tool_calls

        metrics: dict[str, Any] | None | Unset
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, AgentInstanceHistoryItemMetrics1):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        model = self.model

        provider = self.provider

        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        system_prompt: list[dict[str, Any]] | None | Unset
        if isinstance(self.system_prompt, Unset):
            system_prompt = UNSET
        elif isinstance(self.system_prompt, list):
            system_prompt = []
            for system_prompt_type_0_item_data in self.system_prompt:
                system_prompt_type_0_item: dict[str, Any]
                if isinstance(system_prompt_type_0_item_data, TextContent):
                    system_prompt_type_0_item = system_prompt_type_0_item_data.to_dict()
                elif isinstance(system_prompt_type_0_item_data, DocumentContent):
                    system_prompt_type_0_item = system_prompt_type_0_item_data.to_dict()
                else:
                    system_prompt_type_0_item = system_prompt_type_0_item_data.to_dict()

                system_prompt.append(system_prompt_type_0_item)

        else:
            system_prompt = self.system_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "historyItemId": history_item_id,
                "loopIteration": loop_iteration,
                "role": role,
                "content": content,
                "producedAt": produced_at,
            }
        )
        if tool_calls is not UNSET:
            field_dict["toolCalls"] = tool_calls
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if tools is not UNSET:
            field_dict["tools"] = tools
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if limits is not UNSET:
            field_dict["limits"] = limits
        if system_prompt is not UNSET:
            field_dict["systemPrompt"] = system_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_history_item_limits import (
            AgentInstanceHistoryItemLimits,
        )
        from ..models.agent_instance_history_item_metrics_1 import (
            AgentInstanceHistoryItemMetrics1,
        )
        from ..models.agent_instance_tool_call import AgentInstanceToolCall
        from ..models.agent_tool import AgentTool
        from ..models.document_content import DocumentContent
        from ..models.object_content import ObjectContent
        from ..models.text_content import TextContent

        d = dict(src_dict)
        history_item_id = d.pop("historyItemId")

        loop_iteration = d.pop("loopIteration")

        role = AgentInstanceHistoryItemRole(d.pop("role"))

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

        produced_at = isoparse(d.pop("producedAt"))

        def _parse_tool_calls(
            data: object,
        ) -> list[AgentInstanceToolCall] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tool_calls_type_0: list[AgentInstanceToolCall] = []
                _tool_calls_type_0 = cast(list[Any], data)
                for tool_calls_type_0_item_data in _tool_calls_type_0:
                    tool_calls_type_0_item = AgentInstanceToolCall.from_dict(
                        tool_calls_type_0_item_data
                    )

                    tool_calls_type_0.append(tool_calls_type_0_item)

                return tool_calls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentInstanceToolCall] | None | Unset, data)

        tool_calls = _parse_tool_calls(d.pop("toolCalls", UNSET))

        def _parse_metrics(
            data: object,
        ) -> AgentInstanceHistoryItemMetrics1 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_agent_instance_history_item_metrics_1_type_0 = (
                    AgentInstanceHistoryItemMetrics1.from_dict(data)
                )

                return componentsschemas_agent_instance_history_item_metrics_1_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentInstanceHistoryItemMetrics1 | None | Unset, data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        def _parse_tools(data: object) -> list[AgentTool] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0: list[AgentTool] = []
                _tools_type_0 = cast(list[Any], data)
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = AgentTool.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentTool] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: AgentInstanceHistoryItemLimits | Unset
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = AgentInstanceHistoryItemLimits.from_dict(_limits)

        def _parse_system_prompt(
            data: object,
        ) -> list[DocumentContent | ObjectContent | TextContent] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                system_prompt_type_0 = []
                _system_prompt_type_0 = data
                for system_prompt_type_0_item_data in _system_prompt_type_0:

                    def _parse_system_prompt_type_0_item(
                        data: object,
                    ) -> DocumentContent | ObjectContent | TextContent:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()

                            data = cast(dict[str, Any], data)
                            componentsschemas_agent_instance_message_content_type_0 = (
                                TextContent.from_dict(data)
                            )

                            return (
                                componentsschemas_agent_instance_message_content_type_0
                            )
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()

                            data = cast(dict[str, Any], data)
                            componentsschemas_agent_instance_message_content_type_1 = (
                                DocumentContent.from_dict(data)
                            )

                            return (
                                componentsschemas_agent_instance_message_content_type_1
                            )
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()

                        data = cast(dict[str, Any], data)
                        componentsschemas_agent_instance_message_content_type_2 = (
                            ObjectContent.from_dict(data)
                        )

                        return componentsschemas_agent_instance_message_content_type_2

                    system_prompt_type_0_item = _parse_system_prompt_type_0_item(
                        system_prompt_type_0_item_data
                    )

                    system_prompt_type_0.append(system_prompt_type_0_item)

                return system_prompt_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[DocumentContent | ObjectContent | TextContent] | None | Unset, data
            )

        system_prompt = _parse_system_prompt(d.pop("systemPrompt", UNSET))

        agent_instance_history_item = cls(
            history_item_id=history_item_id,
            loop_iteration=loop_iteration,
            role=role,
            content=content,
            produced_at=produced_at,
            tool_calls=tool_calls,
            metrics=metrics,
            tools=tools,
            model=model,
            provider=provider,
            limits=limits,
            system_prompt=system_prompt,
        )

        agent_instance_history_item.additional_properties = d
        return agent_instance_history_item

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
