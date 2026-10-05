from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_balance_response_state import ClusterBalanceResponseState

if TYPE_CHECKING:
    from ..models.cluster_balance_response_last_completed_rebalance import (
        ClusterBalanceResponseLastCompletedRebalance,
    )
    from ..models.cluster_balance_response_running_rebalance import (
        ClusterBalanceResponseRunningRebalance,
    )
    from ..models.cluster_rebalance_partition import ClusterRebalancePartition


T = TypeVar("T", bound="ClusterBalanceResponse")


@_attrs_define
class ClusterBalanceResponse:
    """The cluster's current per-partition balance state, the running rebalance, and the last completed rebalance.

    Attributes:
        state (ClusterBalanceResponseState): The cluster's aggregate balance state as of the time of the request.
            Example: UNBALANCED.
        partitions (list[ClusterRebalancePartition]): The balance state of each partition as of the time of the request.
        running_rebalance (ClusterBalanceResponseRunningRebalance | None): Normally the rebalance currently running, or
            absent if no rebalance is running. For a dry-run response, this is instead the unexecuted plan of that dry run.
        last_completed_rebalance (ClusterBalanceResponseLastCompletedRebalance | None): The last completed non-dry-run
            rebalance this coordinator finished.
    """

    state: ClusterBalanceResponseState
    partitions: list[ClusterRebalancePartition]
    running_rebalance: ClusterBalanceResponseRunningRebalance | None
    last_completed_rebalance: ClusterBalanceResponseLastCompletedRebalance | None
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.cluster_balance_response_last_completed_rebalance import (
            ClusterBalanceResponseLastCompletedRebalance,
        )
        from ..models.cluster_balance_response_running_rebalance import (
            ClusterBalanceResponseRunningRebalance,
        )

        state = self.state.value

        partitions: list[dict[str, Any]] = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        running_rebalance: dict[str, Any] | None
        if isinstance(self.running_rebalance, ClusterBalanceResponseRunningRebalance):
            running_rebalance = self.running_rebalance.to_dict()
        else:
            running_rebalance = self.running_rebalance

        last_completed_rebalance: dict[str, Any] | None
        if isinstance(
            self.last_completed_rebalance, ClusterBalanceResponseLastCompletedRebalance
        ):
            last_completed_rebalance = self.last_completed_rebalance.to_dict()
        else:
            last_completed_rebalance = self.last_completed_rebalance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "partitions": partitions,
                "runningRebalance": running_rebalance,
                "lastCompletedRebalance": last_completed_rebalance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_balance_response_last_completed_rebalance import (
            ClusterBalanceResponseLastCompletedRebalance,
        )
        from ..models.cluster_balance_response_running_rebalance import (
            ClusterBalanceResponseRunningRebalance,
        )
        from ..models.cluster_rebalance_partition import ClusterRebalancePartition

        d = dict(src_dict)
        state = ClusterBalanceResponseState(d.pop("state"))

        partitions: list[ClusterRebalancePartition] = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = ClusterRebalancePartition.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        def _parse_running_rebalance(
            data: object,
        ) -> ClusterBalanceResponseRunningRebalance | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_cluster_balance_response_running_rebalance_type_0 = (
                    ClusterBalanceResponseRunningRebalance.from_dict(data)
                )

                return (
                    componentsschemas_cluster_balance_response_running_rebalance_type_0
                )
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClusterBalanceResponseRunningRebalance | None, data)

        running_rebalance = _parse_running_rebalance(d.pop("runningRebalance"))

        def _parse_last_completed_rebalance(
            data: object,
        ) -> ClusterBalanceResponseLastCompletedRebalance | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_cluster_balance_response_last_completed_rebalance_type_0 = ClusterBalanceResponseLastCompletedRebalance.from_dict(
                    data
                )

                return componentsschemas_cluster_balance_response_last_completed_rebalance_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClusterBalanceResponseLastCompletedRebalance | None, data)

        last_completed_rebalance = _parse_last_completed_rebalance(
            d.pop("lastCompletedRebalance")
        )

        cluster_balance_response = cls(
            state=state,
            partitions=partitions,
            running_rebalance=running_rebalance,
            last_completed_rebalance=last_completed_rebalance,
        )

        cluster_balance_response.additional_properties = d
        return cluster_balance_response

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
