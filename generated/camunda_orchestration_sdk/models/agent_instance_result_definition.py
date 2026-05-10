from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceResultDefinition")


@_attrs_define
class AgentInstanceResultDefinition:
    """The static definition of the agent, including model, provider, and system prompt.

    Attributes:
        model (str): The LLM model identifier (for example, gpt-4o).
        provider (str): The LLM provider (for example, openai or anthropic).
        system_prompt (str): The system prompt configured for this agent instance.
    """

    model: str
    provider: str
    system_prompt: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        provider = self.provider

        system_prompt = self.system_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "provider": provider,
                "systemPrompt": system_prompt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        provider = d.pop("provider")

        system_prompt = d.pop("systemPrompt")

        agent_instance_result_definition = cls(
            model=model,
            provider=provider,
            system_prompt=system_prompt,
        )

        agent_instance_result_definition.additional_properties = d
        return agent_instance_result_definition

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
