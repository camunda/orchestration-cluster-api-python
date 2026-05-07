from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceResultLimits")


@_attrs_define
class AgentInstanceResultLimits:
    """The configured limits for this agent instance, set once at creation.

    Attributes:
        max_model_calls (int): Maximum LLM calls allowed. -1 if no limit is configured.
        max_tool_calls (int): Maximum tool calls allowed. -1 if no limit is configured.
        max_tokens (int): Maximum total tokens allowed. -1 if no limit is configured.
    """

    max_model_calls: int
    max_tool_calls: int
    max_tokens: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        max_model_calls = self.max_model_calls

        max_tool_calls = self.max_tool_calls

        max_tokens = self.max_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "maxModelCalls": max_model_calls,
                "maxToolCalls": max_tool_calls,
                "maxTokens": max_tokens,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_model_calls = d.pop("maxModelCalls")

        max_tool_calls = d.pop("maxToolCalls")

        max_tokens = d.pop("maxTokens")

        agent_instance_result_limits = cls(
            max_model_calls=max_model_calls,
            max_tool_calls=max_tool_calls,
            max_tokens=max_tokens,
        )

        agent_instance_result_limits.additional_properties = d
        return agent_instance_result_limits

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
