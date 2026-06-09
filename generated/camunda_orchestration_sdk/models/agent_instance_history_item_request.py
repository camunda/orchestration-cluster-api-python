from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_history_item_request_role import (
    AgentInstanceHistoryItemRequestRole,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
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
    """Request to append a single history item to an agent instance's conversation history.

    Attributes:
        element_instance_key (str): The key of the currently-active element instance.
             Example: 2251799813686789.
        job_key (str): The key of the current job activation during which this history item was produced. Example:
            2251799813653498.
        job_lease (str): Opaque lease token received from the job activation response.
        role (AgentInstanceHistoryItemRequestRole): The role of this history item in the conversation.
        content (list[DocumentContent | ObjectContent | TextContent]): The content blocks of this history item.
        produced_at (datetime.datetime): The connector-side timestamp of when this message was produced.
        iteration (int | None | Unset): Sequential iteration number this item belongs to. Omit if not grouping items
            into iterations. Example: 1.
        tool_calls (list[AgentInstanceToolCall] | None | Unset): Tool calls associated with this history item.
            For ASSISTANT items: tool calls dispatched by this LLM response, with arguments populated.
            For TOOL_RESULT items: single-entry array referencing the originating tool call, with arguments null.
            Omit for USER items.
        metrics (AgentInstanceHistoryItemRequestMetrics | None | Unset): Per-call token and latency metrics. Present on
            ASSISTANT items only.
    """

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

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance_history_item_request_metrics import (
            AgentInstanceHistoryItemRequestMetrics,
        )
        from ..models.document_content import DocumentContent
        from ..models.text_content import TextContent

        element_instance_key = self.element_instance_key

        job_key = self.job_key

        job_lease = self.job_lease

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

        iteration: int | None | Unset
        if isinstance(self.iteration, Unset):
            iteration = UNSET
        else:
            iteration = self.iteration

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
        elif isinstance(self.metrics, AgentInstanceHistoryItemRequestMetrics):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
                "jobLease": job_lease,
                "role": role,
                "content": content,
                "producedAt": produced_at,
            }
        )
        if iteration is not UNSET:
            field_dict["iteration"] = iteration
        if tool_calls is not UNSET:
            field_dict["toolCalls"] = tool_calls
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

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
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        job_key = JobKey(d.pop("jobKey"))

        job_lease = d.pop("jobLease")

        role = AgentInstanceHistoryItemRequestRole(d.pop("role"))

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

        def _parse_iteration(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        iteration = _parse_iteration(d.pop("iteration", UNSET))

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
        ) -> AgentInstanceHistoryItemRequestMetrics | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
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
            return cast(AgentInstanceHistoryItemRequestMetrics | None | Unset, data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        agent_instance_history_item_request = cls(
            element_instance_key=element_instance_key,
            job_key=job_key,
            job_lease=job_lease,
            role=role,
            content=content,
            produced_at=produced_at,
            iteration=iteration,
            tool_calls=tool_calls,
            metrics=metrics,
        )

        agent_instance_history_item_request.additional_properties = d
        return agent_instance_history_item_request

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
