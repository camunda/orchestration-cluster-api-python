from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AgentInstanceKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_instance_created_history_item import (
        AgentInstanceCreatedHistoryItem,
    )


T = TypeVar("T", bound="AgentInstanceCreationResult")


@_attrs_define
class AgentInstanceCreationResult:
    """Response returned after successfully creating an agent instance.

    Attributes:
        agent_instance_key (str): The system-generated key for the created agent instance. Example: 4503599627370496.
        created_history (list[AgentInstanceCreatedHistoryItem]): One entry per history item submitted in the request, in
            request order.
            Empty when no history items were submitted.
    """

    agent_instance_key: AgentInstanceKey
    created_history: list[AgentInstanceCreatedHistoryItem]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        agent_instance_key = self.agent_instance_key

        created_history: list[dict[str, Any]] = []
        for created_history_item_data in self.created_history:
            created_history_item = created_history_item_data.to_dict()
            created_history.append(created_history_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agentInstanceKey": agent_instance_key,
                "createdHistory": created_history,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_created_history_item import (
            AgentInstanceCreatedHistoryItem,
        )

        d = dict(src_dict)
        agent_instance_key = AgentInstanceKey(d.pop("agentInstanceKey"))

        created_history: list[AgentInstanceCreatedHistoryItem] = []
        _created_history = d.pop("createdHistory")
        for created_history_item_data in _created_history:
            created_history_item = AgentInstanceCreatedHistoryItem.from_dict(
                created_history_item_data
            )

            created_history.append(created_history_item)

        agent_instance_creation_result = cls(
            agent_instance_key=agent_instance_key,
            created_history=created_history,
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
