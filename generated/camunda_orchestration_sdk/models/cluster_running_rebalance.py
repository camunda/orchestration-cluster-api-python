from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.cluster_rebalance_operation_partition import (
        ClusterRebalanceOperationPartition,
    )


T = TypeVar("T", bound="ClusterRunningRebalance")


@_attrs_define
class ClusterRunningRebalance:
    """The rebalance currently running.

    Attributes:
        rebalance_id (int): The ID of this rebalance.
        partitions (list[ClusterRebalanceOperationPartition]): Every partition in the rebalance plan and its progress
            within this rebalance.
        started_at (datetime.datetime): When this rebalance was created.
        dry_run (bool): Whether this rebalance is a dry run.
        cancel_requested (bool): Whether cancellation has been requested.
    """

    rebalance_id: int
    partitions: list[ClusterRebalanceOperationPartition]
    started_at: datetime.datetime
    dry_run: bool
    cancel_requested: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        rebalance_id = self.rebalance_id

        partitions: list[dict[str, Any]] = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        started_at = self.started_at.isoformat()

        dry_run = self.dry_run

        cancel_requested = self.cancel_requested

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rebalanceId": rebalance_id,
                "partitions": partitions,
                "startedAt": started_at,
                "dryRun": dry_run,
                "cancelRequested": cancel_requested,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_rebalance_operation_partition import (
            ClusterRebalanceOperationPartition,
        )

        d = dict(src_dict)
        rebalance_id = d.pop("rebalanceId")

        partitions: list[ClusterRebalanceOperationPartition] = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = ClusterRebalanceOperationPartition.from_dict(
                partitions_item_data
            )

            partitions.append(partitions_item)

        started_at = isoparse(d.pop("startedAt"))

        dry_run = d.pop("dryRun")

        cancel_requested = d.pop("cancelRequested")

        cluster_running_rebalance = cls(
            rebalance_id=rebalance_id,
            partitions=partitions,
            started_at=started_at,
            dry_run=dry_run,
            cancel_requested=cancel_requested,
        )

        cluster_running_rebalance.additional_properties = d
        return cluster_running_rebalance

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
