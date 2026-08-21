from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.document_content import DocumentContent
    from ..models.object_content import ObjectContent
    from ..models.text_content import TextContent


T = TypeVar("T", bound="AgentInstanceDefinitionResult")


@_attrs_define
class AgentInstanceDefinitionResult:
    """The definition of an agent instance. Set at creation, but can change later via a
    CONFIGURATION history item.

        Attributes:
            model (str): The LLM model identifier (for example, gpt-4o).
            provider (str): The LLM provider (for example, openai or anthropic).
            system_prompt (list[DocumentContent | ObjectContent | TextContent]): The system prompt configured for this agent
                instance, as content blocks.
    """

    model: str
    provider: str
    system_prompt: list[DocumentContent | ObjectContent | TextContent]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.document_content import DocumentContent
        from ..models.text_content import TextContent

        model = self.model

        provider = self.provider

        system_prompt: list[dict[str, Any]] = []
        for system_prompt_item_data in self.system_prompt:
            system_prompt_item: dict[str, Any]
            if isinstance(system_prompt_item_data, TextContent):
                system_prompt_item = system_prompt_item_data.to_dict()
            elif isinstance(system_prompt_item_data, DocumentContent):
                system_prompt_item = system_prompt_item_data.to_dict()
            else:
                system_prompt_item = system_prompt_item_data.to_dict()

            system_prompt.append(system_prompt_item)

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
        from ..models.document_content import DocumentContent
        from ..models.object_content import ObjectContent
        from ..models.text_content import TextContent

        d = dict(src_dict)
        model = d.pop("model")

        provider = d.pop("provider")

        system_prompt: list[DocumentContent | ObjectContent | TextContent] = []
        _system_prompt = d.pop("systemPrompt")
        for system_prompt_item_data in _system_prompt:

            def _parse_system_prompt_item(
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

            system_prompt_item = _parse_system_prompt_item(system_prompt_item_data)

            system_prompt.append(system_prompt_item)

        agent_instance_definition_result = cls(
            model=model,
            provider=provider,
            system_prompt=system_prompt,
        )

        agent_instance_definition_result.additional_properties = d
        return agent_instance_definition_result

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
