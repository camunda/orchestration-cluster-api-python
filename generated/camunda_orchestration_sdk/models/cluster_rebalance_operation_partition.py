from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_rebalance_operation_partition_progress import (
    ClusterRebalanceOperationPartitionProgress,
)
from ..models.cluster_rebalance_operation_partition_result import (
    ClusterRebalanceOperationPartitionResult,
)

T = TypeVar("T", bound="ClusterRebalanceOperationPartition")


@_attrs_define
class ClusterRebalanceOperationPartition:
    """One partition's plan, progress, and outcome within a rebalance.

    Attributes:
        partition_id (int): The unique ID of this partition, within its physical tenant. Example: 1.
        physical_tenant_id (str): The partition group this partition belongs to. Example: default.
        current_leader (None | str): The leader last observed by this rebalance, or absent if there was no leader.
            Example: 0.
        desired_leader (str): The leader selected when this rebalance was planned. Example: 1.
        progress (ClusterRebalanceOperationPartitionProgress): Where this rebalance has reached for the partition.
        result (ClusterRebalanceOperationPartitionResult): The terminal outcome, present only when progress is
            COMPLETED.
    """

    partition_id: int
    physical_tenant_id: str
    current_leader: None | str
    desired_leader: str
    progress: ClusterRebalanceOperationPartitionProgress
    result: ClusterRebalanceOperationPartitionResult
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        partition_id = self.partition_id

        physical_tenant_id = self.physical_tenant_id

        current_leader: None | str
        current_leader = self.current_leader

        desired_leader = self.desired_leader

        progress = self.progress.value

        result = self.result.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "physicalTenantId": physical_tenant_id,
                "currentLeader": current_leader,
                "desiredLeader": desired_leader,
                "progress": progress,
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        physical_tenant_id = d.pop("physicalTenantId")

        def _parse_current_leader(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        current_leader = _parse_current_leader(d.pop("currentLeader"))

        desired_leader = d.pop("desiredLeader")

        progress = ClusterRebalanceOperationPartitionProgress(d.pop("progress"))

        result = ClusterRebalanceOperationPartitionResult(d.pop("result"))

        cluster_rebalance_operation_partition = cls(
            partition_id=partition_id,
            physical_tenant_id=physical_tenant_id,
            current_leader=current_leader,
            desired_leader=desired_leader,
            progress=progress,
            result=result,
        )

        cluster_rebalance_operation_partition.additional_properties = d
        return cluster_rebalance_operation_partition

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
