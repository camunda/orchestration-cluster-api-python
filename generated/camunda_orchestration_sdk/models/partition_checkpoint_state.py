from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.partition_checkpoint_state_checkpoint_type import (
    PartitionCheckpointStateCheckpointType,
)

T = TypeVar("T", bound="PartitionCheckpointState")


@_attrs_define
class PartitionCheckpointState:
    """Detailed information about the checkpoint state for a given partition.

    Attributes:
        checkpoint_id (int): The id of the checkpoint. Example: 1.
        checkpoint_type (PartitionCheckpointStateCheckpointType): The type of the checkpoint. Example: MARKER.
        partition_id (int): The id of the partition. Example: 3.
        checkpoint_position (int): The log position of the checkpoint. Example: 1500.
        checkpoint_timestamp (datetime.datetime): The timestamp at which the checkpoint was created. Example:
            2020-01-01T00:00:00Z.
    """

    checkpoint_id: int
    checkpoint_type: PartitionCheckpointStateCheckpointType
    partition_id: int
    checkpoint_position: int
    checkpoint_timestamp: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id = self.checkpoint_id

        checkpoint_type = self.checkpoint_type.value

        partition_id = self.partition_id

        checkpoint_position = self.checkpoint_position

        checkpoint_timestamp = self.checkpoint_timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpointId": checkpoint_id,
                "checkpointType": checkpoint_type,
                "partitionId": partition_id,
                "checkpointPosition": checkpoint_position,
                "checkpointTimestamp": checkpoint_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checkpoint_id = d.pop("checkpointId")

        checkpoint_type = PartitionCheckpointStateCheckpointType(
            d.pop("checkpointType")
        )

        partition_id = d.pop("partitionId")

        checkpoint_position = d.pop("checkpointPosition")

        checkpoint_timestamp = isoparse(d.pop("checkpointTimestamp"))

        partition_checkpoint_state = cls(
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            partition_id=partition_id,
            checkpoint_position=checkpoint_position,
            checkpoint_timestamp=checkpoint_timestamp,
        )

        partition_checkpoint_state.additional_properties = d
        return partition_checkpoint_state

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
