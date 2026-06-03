from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentTool")


@_attrs_define
class AgentTool:
    """A tool available to the agent.

    Attributes:
        name (str): The tool name as visible to the LLM.
        description (None | str): A human-readable description of the tool.
        element_id (None | str): The BPMN element ID of the tool element within the ad-hoc sub-process.
    """

    name: str
    description: None | str
    element_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description: None | str
        description = self.description

        element_id: None | str
        element_id = self.element_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "elementId": element_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        def _parse_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        element_id = _parse_element_id(d.pop("elementId"))

        agent_tool = cls(
            name=name,
            description=description,
            element_id=element_id,
        )

        agent_tool.additional_properties = d
        return agent_tool

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
