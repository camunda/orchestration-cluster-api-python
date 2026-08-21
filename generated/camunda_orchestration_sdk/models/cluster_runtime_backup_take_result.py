from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_runtime_backup_take_result_cluster_runtime_backup_take_outcome import (
    ClusterRuntimeBackupTakeResultClusterRuntimeBackupTakeOutcome,
)

T = TypeVar("T", bound="ClusterRuntimeBackupTakeResult")


@_attrs_define
class ClusterRuntimeBackupTakeResult:
    """Whether one physical tenant's runtime backup was triggered, and under which id it can be monitored and deleted.

    Attributes:
        physical_tenant_id (str): The id of the physical tenant. Example: default.
        backup_id (int | None): The id to monitor or delete this physical tenant's backup by: the id it is running under
            when `TRIGGERED` — the requested one, or the one the tenant generated when ids are generated — and the requested
            id to check when `UNKNOWN`. Null when the tenant is known to be running no backup, and also when an `UNKNOWN`
            tenant generates its own ids, because the id it may be running under was never reported; list that tenant's
            backups to find it. Example: 1.
        outcome (ClusterRuntimeBackupTakeResultClusterRuntimeBackupTakeOutcome): What this physical tenant did with the
            trigger. Example: TRIGGERED.
        reason (None | str): Why this physical tenant reported no triggered backup. Null when it was triggered.
    """

    physical_tenant_id: str
    backup_id: int | None
    outcome: ClusterRuntimeBackupTakeResultClusterRuntimeBackupTakeOutcome
    reason: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id = self.physical_tenant_id

        backup_id: int | None
        backup_id = self.backup_id

        outcome = self.outcome.value

        reason: None | str
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "backupId": backup_id,
                "outcome": outcome,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        physical_tenant_id = d.pop("physicalTenantId")

        def _parse_backup_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        backup_id = _parse_backup_id(d.pop("backupId"))

        outcome = ClusterRuntimeBackupTakeResultClusterRuntimeBackupTakeOutcome(
            d.pop("outcome")
        )

        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))

        cluster_runtime_backup_take_result = cls(
            physical_tenant_id=physical_tenant_id,
            backup_id=backup_id,
            outcome=outcome,
            reason=reason,
        )

        cluster_runtime_backup_take_result.additional_properties = d
        return cluster_runtime_backup_take_result

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
