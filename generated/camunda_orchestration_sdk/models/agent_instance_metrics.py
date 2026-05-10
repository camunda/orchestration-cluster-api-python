from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceMetrics")


@_attrs_define
class AgentInstanceMetrics:
    """Aggregated metrics for an agent instance across all model calls.

    Attributes:
        input_tokens (int): Total input tokens consumed across all model calls.
        output_tokens (int): Total output tokens produced across all model calls.
        model_calls (int): Total number of LLM calls made.
        tool_calls (int): Total number of tool calls made.
    """

    input_tokens: int
    output_tokens: int
    model_calls: int
    tool_calls: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        model_calls = self.model_calls

        tool_calls = self.tool_calls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
                "modelCalls": model_calls,
                "toolCalls": tool_calls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        model_calls = d.pop("modelCalls")

        tool_calls = d.pop("toolCalls")

        agent_instance_metrics = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_calls=model_calls,
            tool_calls=tool_calls,
        )

        agent_instance_metrics.additional_properties = d
        return agent_instance_metrics

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
