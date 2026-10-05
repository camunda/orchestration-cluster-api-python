from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.restore_partition_status_state import RestorePartitionStatusState

T = TypeVar("T", bound="RestorePartitionStatus")


@_attrs_define
class RestorePartitionStatus:
    """The restore status of a single partition on a broker.

    Attributes:
        partition_id (int): The ID of the partition. Example: 1.
        state (RestorePartitionStatusState): The restore state of the partition. Example: RESTORING.
        backup_ids (list[int]): The IDs of the backups this partition is restored from. Example: [100, 101].
        completed_at (datetime.datetime | None): The time the partition was restored, as an ISO 8601 timestamp; null
            unless the partition state is `RESTORED`. Example: 2024-01-01T10:02:00Z.
    """

    partition_id: int
    state: RestorePartitionStatusState
    backup_ids: list[int]
    completed_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        partition_id = self.partition_id

        state = self.state.value

        backup_ids = self.backup_ids

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "state": state,
                "backupIds": backup_ids,
                "completedAt": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        state = RestorePartitionStatusState(d.pop("state"))

        backup_ids = cast(list[int], d.pop("backupIds"))

        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completedAt"))

        restore_partition_status = cls(
            partition_id=partition_id,
            state=state,
            backup_ids=backup_ids,
            completed_at=completed_at,
        )

        restore_partition_status.additional_properties = d
        return restore_partition_status

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
