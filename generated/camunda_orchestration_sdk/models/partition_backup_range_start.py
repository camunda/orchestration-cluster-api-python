from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.partition_backup_range_start_backup_type import (
    PartitionBackupRangeStartBackupType,
)

T = TypeVar("T", bound="PartitionBackupRangeStart")


@_attrs_define
class PartitionBackupRangeStart:
    """The oldest backup in the range.

    Attributes:
        checkpoint_id (int): The id of the checkpoint this backup is based on. Example: 1.
        checkpoint_type (PartitionBackupRangeStartBackupType): The type of the backup. Example: SCHEDULED_BACKUP.
        partition_id (int | None): The id of the partition. Omitted when nested inside a backup range's `start`/`end`,
            where the partition is already identified by the enclosing range.
             Example: 3.
        checkpoint_position (int): The log position of the checkpoint this backup is based on. Example: 1500.
        first_log_position (int): The first log position included in this backup. Example: 5.
        checkpoint_timestamp (datetime.datetime): The timestamp at which the checkpoint was created. Example:
            2020-01-01T00:00:00Z.
    """

    checkpoint_id: int
    checkpoint_type: PartitionBackupRangeStartBackupType
    partition_id: int | None
    checkpoint_position: int
    first_log_position: int
    checkpoint_timestamp: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id = self.checkpoint_id

        checkpoint_type = self.checkpoint_type.value

        partition_id: int | None
        partition_id = self.partition_id

        checkpoint_position = self.checkpoint_position

        first_log_position = self.first_log_position

        checkpoint_timestamp = self.checkpoint_timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpointId": checkpoint_id,
                "checkpointType": checkpoint_type,
                "partitionId": partition_id,
                "checkpointPosition": checkpoint_position,
                "firstLogPosition": first_log_position,
                "checkpointTimestamp": checkpoint_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checkpoint_id = d.pop("checkpointId")

        checkpoint_type = PartitionBackupRangeStartBackupType(d.pop("checkpointType"))

        def _parse_partition_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        partition_id = _parse_partition_id(d.pop("partitionId"))

        checkpoint_position = d.pop("checkpointPosition")

        first_log_position = d.pop("firstLogPosition")

        checkpoint_timestamp = isoparse(d.pop("checkpointTimestamp"))

        partition_backup_range_start = cls(
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            partition_id=partition_id,
            checkpoint_position=checkpoint_position,
            first_log_position=first_log_position,
            checkpoint_timestamp=checkpoint_timestamp,
        )

        partition_backup_range_start.additional_properties = d
        return partition_backup_range_start

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
