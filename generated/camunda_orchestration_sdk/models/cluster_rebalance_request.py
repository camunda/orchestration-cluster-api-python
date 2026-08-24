from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ClusterRebalanceRequest")


@_attrs_define
class ClusterRebalanceRequest:
    """The settings to run a given rebalance with. Every setting is optional; an absent request body is equivalent to a
    body with every field absent, and means "use the configured settings".

        Attributes:
            replication_lag_threshold (int | Unset): The highest replication lag (in bytes) that a desired leader may have
                for its transfer to be accepted. Example: 8388608.
            replication_timeout (str | Unset): How long a partition may stay frozen waiting for its desired leader to catch
                up (as a positive ISO-8601 duration). Example: PT10S.
            max_transfer_attempts (int | Unset): How many times a current leader may prompt the desired leader to take over
                leadership before giving up. Example: 3.
            leader_wait_timeout (str | Unset): How long the coordinator waits for a partition without a leader to acquire
                one before reporting `NO_LEADER` and moving on (as a positive ISO-8601 duration). Example: PT1M.
    """

    replication_lag_threshold: int | Unset = UNSET
    replication_timeout: str | Unset = UNSET
    max_transfer_attempts: int | Unset = UNSET
    leader_wait_timeout: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        replication_lag_threshold = self.replication_lag_threshold

        replication_timeout = self.replication_timeout

        max_transfer_attempts = self.max_transfer_attempts

        leader_wait_timeout = self.leader_wait_timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if replication_lag_threshold is not UNSET:
            field_dict["replicationLagThreshold"] = replication_lag_threshold
        if replication_timeout is not UNSET:
            field_dict["replicationTimeout"] = replication_timeout
        if max_transfer_attempts is not UNSET:
            field_dict["maxTransferAttempts"] = max_transfer_attempts
        if leader_wait_timeout is not UNSET:
            field_dict["leaderWaitTimeout"] = leader_wait_timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        replication_lag_threshold = d.pop("replicationLagThreshold", UNSET)

        replication_timeout = d.pop("replicationTimeout", UNSET)

        max_transfer_attempts = d.pop("maxTransferAttempts", UNSET)

        leader_wait_timeout = d.pop("leaderWaitTimeout", UNSET)

        cluster_rebalance_request = cls(
            replication_lag_threshold=replication_lag_threshold,
            replication_timeout=replication_timeout,
            max_transfer_attempts=max_transfer_attempts,
            leader_wait_timeout=leader_wait_timeout,
        )

        cluster_rebalance_request.additional_properties = d
        return cluster_rebalance_request

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
