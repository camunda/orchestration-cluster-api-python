from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.partition_backup_info_runtime_backup_state import (
    PartitionBackupInfoRuntimeBackupState,
)

T = TypeVar("T", bound="PartitionBackupInfo")


@_attrs_define
class PartitionBackupInfo:
    """Detailed info of the backup for a given partition.

    Attributes:
        partition_id (int): The id of the partition. Example: 3.
        state (PartitionBackupInfoRuntimeBackupState): The state of the backup on this partition. Example: IN_PROGRESS.
        failure_reason (None | str): Failure reason if the state is 'FAILED'.
        created_at (datetime.datetime | None): The timestamp at which the backup was started on this partition. Example:
            2022-09-15T13:10:38.176514094Z.
        last_updated_at (datetime.datetime | None): The timestamp at which the backup was last updated on this
            partition, e.g. changed
            state from 'IN_PROGRESS' to 'COMPLETED'.
             Example: 2022-09-15T13:10:38.176514094Z.
        snapshot_id (None | str): The id of the snapshot which is included in this backup. Example:
            238632143-55-690906332-690905294.
        first_log_position (int | None): The first log position included in this backup. Example: 5.
        checkpoint_position (int | None): The position of the checkpoint for this backup. Example: 10.
        broker_id (int | None): The id of the broker from which the backup was taken for this partition.
        broker_version (None | str): The version of the broker from which the backup was taken for this partition.
             Example: 8.10.0.
    """

    partition_id: int
    state: PartitionBackupInfoRuntimeBackupState
    failure_reason: None | str
    created_at: datetime.datetime | None
    last_updated_at: datetime.datetime | None
    snapshot_id: None | str
    first_log_position: int | None
    checkpoint_position: int | None
    broker_id: int | None
    broker_version: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        partition_id = self.partition_id

        state = self.state.value

        failure_reason: None | str
        failure_reason = self.failure_reason

        created_at: None | str
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        last_updated_at: None | str
        if isinstance(self.last_updated_at, datetime.datetime):
            last_updated_at = self.last_updated_at.isoformat()
        else:
            last_updated_at = self.last_updated_at

        snapshot_id: None | str
        snapshot_id = self.snapshot_id

        first_log_position: int | None
        first_log_position = self.first_log_position

        checkpoint_position: int | None
        checkpoint_position = self.checkpoint_position

        broker_id: int | None
        broker_id = self.broker_id

        broker_version: None | str
        broker_version = self.broker_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "state": state,
                "failureReason": failure_reason,
                "createdAt": created_at,
                "lastUpdatedAt": last_updated_at,
                "snapshotId": snapshot_id,
                "firstLogPosition": first_log_position,
                "checkpointPosition": checkpoint_position,
                "brokerId": broker_id,
                "brokerVersion": broker_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        state = PartitionBackupInfoRuntimeBackupState(d.pop("state"))

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("createdAt"))

        def _parse_last_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_updated_at_type_0 = isoparse(data)

                return last_updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_updated_at = _parse_last_updated_at(d.pop("lastUpdatedAt"))

        def _parse_snapshot_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        snapshot_id = _parse_snapshot_id(d.pop("snapshotId"))

        def _parse_first_log_position(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        first_log_position = _parse_first_log_position(d.pop("firstLogPosition"))

        def _parse_checkpoint_position(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        checkpoint_position = _parse_checkpoint_position(d.pop("checkpointPosition"))

        def _parse_broker_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        broker_id = _parse_broker_id(d.pop("brokerId"))

        def _parse_broker_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        broker_version = _parse_broker_version(d.pop("brokerVersion"))

        partition_backup_info = cls(
            partition_id=partition_id,
            state=state,
            failure_reason=failure_reason,
            created_at=created_at,
            last_updated_at=last_updated_at,
            snapshot_id=snapshot_id,
            first_log_position=first_log_position,
            checkpoint_position=checkpoint_position,
            broker_id=broker_id,
            broker_version=broker_version,
        )

        partition_backup_info.additional_properties = d
        return partition_backup_info

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
