from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AgentInstanceUpdateRequestMetrics")


@_attrs_define
class AgentInstanceUpdateRequestMetrics:
    """Metric increments to apply to the aggregate counters.

    Attributes:
        input_tokens (int | Unset): Increment to apply to the total input token counter.
        output_tokens (int | Unset): Increment to apply to the total output token counter.
        model_calls (int | Unset): Increment to apply to the total model call counter.
        tool_calls (int | Unset): Increment to apply to the total tool call counter.
    """

    input_tokens: int | Unset = UNSET
    output_tokens: int | Unset = UNSET
    model_calls: int | Unset = UNSET
    tool_calls: int | Unset = UNSET
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
        field_dict.update({})
        if input_tokens is not UNSET:
            field_dict["inputTokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["outputTokens"] = output_tokens
        if model_calls is not UNSET:
            field_dict["modelCalls"] = model_calls
        if tool_calls is not UNSET:
            field_dict["toolCalls"] = tool_calls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_tokens = d.pop("inputTokens", UNSET)

        output_tokens = d.pop("outputTokens", UNSET)

        model_calls = d.pop("modelCalls", UNSET)

        tool_calls = d.pop("toolCalls", UNSET)

        agent_instance_update_request_metrics = cls(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_calls=model_calls,
            tool_calls=tool_calls,
        )

        agent_instance_update_request_metrics.additional_properties = d
        return agent_instance_update_request_metrics

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
