from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceHistoryItemMetrics")


@_attrs_define
class AgentInstanceHistoryItemMetrics:
    """Per-call token and latency metrics for an ASSISTANT history item.

    Attributes:
        input_tokens (int): Input tokens consumed by this LLM call.
        output_tokens (int): Output tokens produced by this LLM call.
        duration_ms (int): Wall-clock duration of the LLM call in milliseconds.
    """

    input_tokens: int
    output_tokens: int
    duration_ms: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        duration_ms = self.duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
                "durationMs": duration_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        duration_ms = d.pop("durationMs")

        agent_instance_history_item_metrics = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            duration_ms=duration_ms,
        )

        agent_instance_history_item_metrics.additional_properties = d
        return agent_instance_history_item_metrics

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
