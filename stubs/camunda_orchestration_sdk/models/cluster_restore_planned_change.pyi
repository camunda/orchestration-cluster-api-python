from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.cluster_restore_await_mode_change_operation import (
    ClusterRestoreAwaitModeChangeOperation,
)
from ..models.cluster_restore_broker_operation import ClusterRestoreBrokerOperation
from ..models.cluster_restore_mode_change_operation import (
    ClusterRestoreModeChangeOperation,
)
from ..models.cluster_restore_partition_operation import (
    ClusterRestorePartitionOperation,
)
from ..models.cluster_restore_partition_restore_operation import (
    ClusterRestorePartitionRestoreOperation,
)

T = TypeVar("T", bound="ClusterRestorePlannedChange")

@_attrs_define
class ClusterRestorePlannedChange:
    physical_tenant_id: None | str
    operations: list[
        ClusterRestoreAwaitModeChangeOperation
        | ClusterRestoreBrokerOperation
        | ClusterRestoreModeChangeOperation
        | ClusterRestorePartitionOperation
        | ClusterRestorePartitionRestoreOperation
    ]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
