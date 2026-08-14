from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="TakeHistoryBackupResponse")


@_attrs_define
class TakeHistoryBackupResponse:
    """Response body for taking a history backup.

    Attributes:
        backup_id (int): The id of the backup that has been scheduled. Example: 1.
        scheduled_snapshots (list[str]): The names of the snapshots that have been scheduled for this backup.
    """

    backup_id: int
    scheduled_snapshots: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        scheduled_snapshots = self.scheduled_snapshots

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backupId": backup_id,
                "scheduledSnapshots": scheduled_snapshots,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backup_id = d.pop("backupId")

        scheduled_snapshots = cast(list[str], d.pop("scheduledSnapshots"))

        take_history_backup_response = cls(
            backup_id=backup_id,
            scheduled_snapshots=scheduled_snapshots,
        )

        take_history_backup_response.additional_properties = d
        return take_history_backup_response

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
