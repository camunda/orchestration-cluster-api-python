from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AgentHistoryItemKey

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceHistoryItemCreationResult")


@_attrs_define
class AgentInstanceHistoryItemCreationResult:
    """Response returned after successfully appending a history item.

    Attributes:
        history_item_key (str): The system-generated key for the created history item. Example: 6755399441055744.
    """

    history_item_key: AgentHistoryItemKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        history_item_key = self.history_item_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "historyItemKey": history_item_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        history_item_key = AgentHistoryItemKey(d.pop("historyItemKey"))

        agent_instance_history_item_creation_result = cls(
            history_item_key=history_item_key,
        )

        agent_instance_history_item_creation_result.additional_properties = d
        return agent_instance_history_item_creation_result

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
