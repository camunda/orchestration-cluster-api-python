from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClusterRestorePartitionRestoreOperation")


@_attrs_define
class ClusterRestorePartitionRestoreOperation:
    """The operation that restores a single partition from the backups resolved for it.

    Attributes:
        operation (str): The type of the operation. Example: PartitionRestoreOperation.
        broker_id (str): The ID of the broker that applies the operation, including its zone if it belongs to one.
            Example: 1.
        partition_id (int): The partition the operation restores. Example: 1.
        backup_ids (list[int]): The IDs of the backups the partition is restored from. Example: [100, 101].
    """

    operation: str
    broker_id: str
    partition_id: int
    backup_ids: list[int]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        operation = self.operation

        broker_id = self.broker_id

        partition_id = self.partition_id

        backup_ids = self.backup_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation": operation,
                "brokerId": broker_id,
                "partitionId": partition_id,
                "backupIds": backup_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation = d.pop("operation")

        broker_id = d.pop("brokerId")

        partition_id = d.pop("partitionId")

        backup_ids = cast(list[int], d.pop("backupIds"))

        cluster_restore_partition_restore_operation = cls(
            operation=operation,
            broker_id=broker_id,
            partition_id=partition_id,
            backup_ids=backup_ids,
        )

        cluster_restore_partition_restore_operation.additional_properties = d
        return cluster_restore_partition_restore_operation

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
