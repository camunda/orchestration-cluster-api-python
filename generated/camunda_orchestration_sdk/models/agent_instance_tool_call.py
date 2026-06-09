from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_instance_tool_call_arguments import (
        AgentInstanceToolCallArguments,
    )


T = TypeVar("T", bound="AgentInstanceToolCall")


@_attrs_define
class AgentInstanceToolCall:
    """A tool call associated with a history item. Used in both ASSISTANT and TOOL_RESULT items.
    ASSISTANT items carry arguments; TOOL_RESULT items carry arguments as null.

        Attributes:
            tool_call_id (str): The LLM-assigned tool call ID. Correlates ASSISTANT items to their matching TOOL_RESULT
                items.
            tool_name (str): The LLM-visible tool name.
            element_id (None | str): The BPMN element ID handling this tool.
            arguments (AgentInstanceToolCallArguments | None): The tool call arguments as provided by the LLM. Null on
                TOOL_RESULT items.
    """

    tool_call_id: str
    tool_name: str
    element_id: None | str
    arguments: AgentInstanceToolCallArguments | None
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_instance_tool_call_arguments import (
            AgentInstanceToolCallArguments,
        )

        tool_call_id = self.tool_call_id

        tool_name = self.tool_name

        element_id: None | str
        element_id = self.element_id

        arguments: dict[str, Any] | None
        if isinstance(self.arguments, AgentInstanceToolCallArguments):
            arguments = self.arguments.to_dict()
        else:
            arguments = self.arguments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "toolCallId": tool_call_id,
                "toolName": tool_name,
                "elementId": element_id,
                "arguments": arguments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_tool_call_arguments import (
            AgentInstanceToolCallArguments,
        )

        d = dict(src_dict)
        tool_call_id = d.pop("toolCallId")

        tool_name = d.pop("toolName")

        def _parse_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        element_id = _parse_element_id(d.pop("elementId"))

        def _parse_arguments(data: object) -> AgentInstanceToolCallArguments | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_agent_instance_tool_call_arguments_type_0 = (
                    AgentInstanceToolCallArguments.from_dict(data)
                )

                return componentsschemas_agent_instance_tool_call_arguments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AgentInstanceToolCallArguments | None, data)

        arguments = _parse_arguments(d.pop("arguments"))

        agent_instance_tool_call = cls(
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            element_id=element_id,
            arguments=arguments,
        )

        agent_instance_tool_call.additional_properties = d
        return agent_instance_tool_call

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
