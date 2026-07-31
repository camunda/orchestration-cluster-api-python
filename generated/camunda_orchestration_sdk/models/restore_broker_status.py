from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.restore_partition_status import RestorePartitionStatus


T = TypeVar("T", bound="RestoreBrokerStatus")


@_attrs_define
class RestoreBrokerStatus:
    """The restore status of a single broker.

    Attributes:
        broker_id (str): The ID of the broker, including its zone if it belongs to one. Example: 1.
        partitions_restored (int): The number of the broker's partitions that have been restored so far. Example: 1.
        partitions_to_restore (int): The total number of the broker's partitions to restore. Example: 3.
        partitions (list[RestorePartitionStatus]): The per-partition restore status for this broker.
    """

    broker_id: str
    partitions_restored: int
    partitions_to_restore: int
    partitions: list[RestorePartitionStatus]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        broker_id = self.broker_id

        partitions_restored = self.partitions_restored

        partitions_to_restore = self.partitions_to_restore

        partitions: list[dict[str, Any]] = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "brokerId": broker_id,
                "partitionsRestored": partitions_restored,
                "partitionsToRestore": partitions_to_restore,
                "partitions": partitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.restore_partition_status import RestorePartitionStatus

        d = dict(src_dict)
        broker_id = d.pop("brokerId")

        partitions_restored = d.pop("partitionsRestored")

        partitions_to_restore = d.pop("partitionsToRestore")

        partitions: list[RestorePartitionStatus] = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = RestorePartitionStatus.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        restore_broker_status = cls(
            broker_id=broker_id,
            partitions_restored=partitions_restored,
            partitions_to_restore=partitions_to_restore,
            partitions=partitions,
        )

        restore_broker_status.additional_properties = d
        return restore_broker_status

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
