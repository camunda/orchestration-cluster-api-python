from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AgentInstanceHistoryItemMetricsRequest")


@_attrs_define
class AgentInstanceHistoryItemMetricsRequest:
    """Per-call token and latency metrics for an ASSISTANT history item, as submitted on a
    create/update request. All fields are optional: omit a field the caller has no value
    for rather than sending it as an explicit null.

        Attributes:
            input_tokens (int | None | Unset): Input tokens consumed by this LLM call. Null when not provided.
            output_tokens (int | None | Unset): Output tokens produced by this LLM call. Null when not provided.
            reasoning_token_count (int | None | Unset): Reasoning tokens consumed by this LLM call. Null when not provided.
            cache_creation_token_count (int | None | Unset): Cache-creation tokens consumed by this LLM call. Null when not
                provided.
            cache_read_token_count (int | None | Unset): Cache-read tokens consumed by this LLM call. Null when not
                provided.
            duration_ms (int | None | Unset): Wall-clock duration of the LLM call in milliseconds. Null when not provided.
    """

    input_tokens: int | None | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    reasoning_token_count: int | None | Unset = UNSET
    cache_creation_token_count: int | None | Unset = UNSET
    cache_read_token_count: int | None | Unset = UNSET
    duration_ms: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        input_tokens: int | None | Unset
        if isinstance(self.input_tokens, Unset):
            input_tokens = UNSET
        else:
            input_tokens = self.input_tokens

        output_tokens: int | None | Unset
        if isinstance(self.output_tokens, Unset):
            output_tokens = UNSET
        else:
            output_tokens = self.output_tokens

        reasoning_token_count: int | None | Unset
        if isinstance(self.reasoning_token_count, Unset):
            reasoning_token_count = UNSET
        else:
            reasoning_token_count = self.reasoning_token_count

        cache_creation_token_count: int | None | Unset
        if isinstance(self.cache_creation_token_count, Unset):
            cache_creation_token_count = UNSET
        else:
            cache_creation_token_count = self.cache_creation_token_count

        cache_read_token_count: int | None | Unset
        if isinstance(self.cache_read_token_count, Unset):
            cache_read_token_count = UNSET
        else:
            cache_read_token_count = self.cache_read_token_count

        duration_ms: int | None | Unset
        if isinstance(self.duration_ms, Unset):
            duration_ms = UNSET
        else:
            duration_ms = self.duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_tokens is not UNSET:
            field_dict["inputTokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["outputTokens"] = output_tokens
        if reasoning_token_count is not UNSET:
            field_dict["reasoningTokenCount"] = reasoning_token_count
        if cache_creation_token_count is not UNSET:
            field_dict["cacheCreationTokenCount"] = cache_creation_token_count
        if cache_read_token_count is not UNSET:
            field_dict["cacheReadTokenCount"] = cache_read_token_count
        if duration_ms is not UNSET:
            field_dict["durationMs"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("inputTokens", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("outputTokens", UNSET))

        def _parse_reasoning_token_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        reasoning_token_count = _parse_reasoning_token_count(
            d.pop("reasoningTokenCount", UNSET)
        )

        def _parse_cache_creation_token_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cache_creation_token_count = _parse_cache_creation_token_count(
            d.pop("cacheCreationTokenCount", UNSET)
        )

        def _parse_cache_read_token_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cache_read_token_count = _parse_cache_read_token_count(
            d.pop("cacheReadTokenCount", UNSET)
        )

        def _parse_duration_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        duration_ms = _parse_duration_ms(d.pop("durationMs", UNSET))

        agent_instance_history_item_metrics_request = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            reasoning_token_count=reasoning_token_count,
            cache_creation_token_count=cache_creation_token_count,
            cache_read_token_count=cache_read_token_count,
            duration_ms=duration_ms,
        )

        agent_instance_history_item_metrics_request.additional_properties = d
        return agent_instance_history_item_metrics_request

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
