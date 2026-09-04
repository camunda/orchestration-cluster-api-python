from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AgentHistoryItemKey, HistoryItemId

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInstanceCreatedHistoryItem")


@_attrs_define
class AgentInstanceCreatedHistoryItem:
    """The outcome of appending a single history item from an update request's
    history batch.

        Attributes:
            history_item_id (str): The historyItemId of the corresponding item in the request, echoed back
                so callers can correlate response entries with request items by id.
                 Example: item-1.
            history_item_key (str): The system-generated key for the history item. When isDuplicate is true,
                this is the key of the original entry, not a new one.
                 Example: 6755399441055744.
            is_duplicate (bool): True if this item had already been recorded and no new AGENT_HISTORY event
                was created for it; false if a new event was created.
    """

    history_item_id: HistoryItemId
    history_item_key: AgentHistoryItemKey
    is_duplicate: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        history_item_id = self.history_item_id

        history_item_key = self.history_item_key

        is_duplicate = self.is_duplicate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "historyItemId": history_item_id,
                "historyItemKey": history_item_key,
                "isDuplicate": is_duplicate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        history_item_id = HistoryItemId(d.pop("historyItemId"))

        history_item_key = AgentHistoryItemKey(d.pop("historyItemKey"))

        is_duplicate = d.pop("isDuplicate")

        agent_instance_created_history_item = cls(
            history_item_id=history_item_id,
            history_item_key=history_item_key,
            is_duplicate=is_duplicate,
        )

        agent_instance_created_history_item.additional_properties = d
        return agent_instance_created_history_item

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
