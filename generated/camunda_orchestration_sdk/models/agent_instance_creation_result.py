from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AgentInstanceKey

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceCreationResult")


@_attrs_define
class AgentInstanceCreationResult:
    """Response returned after successfully creating an agent instance.

    Attributes:
        agent_instance_key (str): The system-generated key for the created agent instance. Example: 4503599627370496.
    """

    agent_instance_key: AgentInstanceKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        agent_instance_key = self.agent_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agentInstanceKey": agent_instance_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_instance_key = AgentInstanceKey(d.pop("agentInstanceKey"))

        agent_instance_creation_result = cls(
            agent_instance_key=agent_instance_key,
        )

        agent_instance_creation_result.additional_properties = d
        return agent_instance_creation_result

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
