from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceHistoryItemMetrics1")


@_attrs_define
class AgentInstanceHistoryItemMetrics1:
    """Per-call token and latency metrics. Present on ASSISTANT items only.

    Attributes:
        input_tokens (int | None): Input tokens consumed by this LLM call. Null when not provided.
        output_tokens (int | None): Output tokens produced by this LLM call. Null when not provided.
        duration_ms (int | None): Wall-clock duration of the LLM call in milliseconds. Null when not provided.
    """

    input_tokens: int | None
    output_tokens: int | None
    duration_ms: int | None
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        input_tokens: int | None
        input_tokens = self.input_tokens

        output_tokens: int | None
        output_tokens = self.output_tokens

        duration_ms: int | None
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

        def _parse_input_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        input_tokens = _parse_input_tokens(d.pop("inputTokens"))

        def _parse_output_tokens(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        output_tokens = _parse_output_tokens(d.pop("outputTokens"))

        def _parse_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_ms = _parse_duration_ms(d.pop("durationMs"))

        agent_instance_history_item_metrics_1 = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            duration_ms=duration_ms,
        )

        agent_instance_history_item_metrics_1.additional_properties = d
        return agent_instance_history_item_metrics_1

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
