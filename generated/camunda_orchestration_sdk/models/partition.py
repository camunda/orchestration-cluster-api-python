from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.partition_health import PartitionHealth
from ..models.partition_role import PartitionRole

T = TypeVar("T", bound="Partition")


@_attrs_define
class Partition:
    """Provides information on a partition within a broker node.

    Attributes:
        partition_id (int): The unique ID of this partition. Example: 1.
        role (PartitionRole): Describes the Raft role of the broker for a given partition. Example: leader.
        health (PartitionHealth): Describes the current health of the partition. Example: healthy.
    """

    partition_id: int
    role: PartitionRole
    health: PartitionHealth
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        partition_id = self.partition_id

        role = self.role.value

        health = self.health.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "role": role,
                "health": health,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        role = PartitionRole(d.pop("role"))

        health = PartitionHealth(d.pop("health"))

        partition = cls(
            partition_id=partition_id,
            role=role,
            health=health,
        )

        partition.additional_properties = d
        return partition

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
