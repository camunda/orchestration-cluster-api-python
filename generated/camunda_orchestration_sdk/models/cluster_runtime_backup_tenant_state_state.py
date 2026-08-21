from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.partition_backup_range import PartitionBackupRange
    from ..models.partition_backup_state import PartitionBackupState
    from ..models.partition_checkpoint_state import PartitionCheckpointState


T = TypeVar("T", bound="ClusterRuntimeBackupTenantStateState")


@_attrs_define
class ClusterRuntimeBackupTenantStateState:
    """The checkpoint and backup state of this physical tenant's partitions.

    Attributes:
        checkpoint_states (list[PartitionCheckpointState]): List of partition checkpoint states.
        backup_states (list[PartitionBackupState]): List of partition backup states.
        ranges (list[PartitionBackupRange]): List of partition backup ranges.
    """

    checkpoint_states: list[PartitionCheckpointState]
    backup_states: list[PartitionBackupState]
    ranges: list[PartitionBackupRange]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        checkpoint_states: list[dict[str, Any]] = []
        for checkpoint_states_item_data in self.checkpoint_states:
            checkpoint_states_item = checkpoint_states_item_data.to_dict()
            checkpoint_states.append(checkpoint_states_item)

        backup_states: list[dict[str, Any]] = []
        for backup_states_item_data in self.backup_states:
            backup_states_item = backup_states_item_data.to_dict()
            backup_states.append(backup_states_item)

        ranges: list[dict[str, Any]] = []
        for ranges_item_data in self.ranges:
            ranges_item = ranges_item_data.to_dict()
            ranges.append(ranges_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkpointStates": checkpoint_states,
                "backupStates": backup_states,
                "ranges": ranges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partition_backup_range import PartitionBackupRange
        from ..models.partition_backup_state import PartitionBackupState
        from ..models.partition_checkpoint_state import PartitionCheckpointState

        d = dict(src_dict)
        checkpoint_states: list[PartitionCheckpointState] = []
        _checkpoint_states = d.pop("checkpointStates")
        for checkpoint_states_item_data in _checkpoint_states:
            checkpoint_states_item = PartitionCheckpointState.from_dict(
                checkpoint_states_item_data
            )

            checkpoint_states.append(checkpoint_states_item)

        backup_states: list[PartitionBackupState] = []
        _backup_states = d.pop("backupStates")
        for backup_states_item_data in _backup_states:
            backup_states_item = PartitionBackupState.from_dict(backup_states_item_data)

            backup_states.append(backup_states_item)

        ranges: list[PartitionBackupRange] = []
        _ranges = d.pop("ranges")
        for ranges_item_data in _ranges:
            ranges_item = PartitionBackupRange.from_dict(ranges_item_data)

            ranges.append(ranges_item)

        cluster_runtime_backup_tenant_state_state = cls(
            checkpoint_states=checkpoint_states,
            backup_states=backup_states,
            ranges=ranges,
        )

        cluster_runtime_backup_tenant_state_state.additional_properties = d
        return cluster_runtime_backup_tenant_state_state

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
