from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_history_backup_tenant_state import ClusterHistoryBackupTenantState

if TYPE_CHECKING:
    from ..models.history_backup_snapshot_info import HistoryBackupSnapshotInfo


T = TypeVar("T", bound="ClusterHistoryBackupTenantInfo")


@_attrs_define
class ClusterHistoryBackupTenantInfo:
    """What a single physical tenant reports for a history backup id.

    Attributes:
        physical_tenant_id (str): The id of the physical tenant. Example: default.
        state (ClusterHistoryBackupTenantState): What a physical tenant reports for a history backup id: the per-tenant
            `HistoryBackupStateCode` extended with `NOT_FOUND` for a tenant that was read and does not hold the backup.
            `NOT_FOUND` is a successful observation, not a failure — a backup that only some physical tenants hold is a
            supported outcome. There is no state for a tenant that could not be read at all, because such a tenant fails the
            whole request. Example: COMPLETED.
        failure_reason (None | str): Reason for failure if the state is 'FAILED'.
        details (list[HistoryBackupSnapshotInfo]): Detailed status of the backup per snapshot on this physical tenant.
            Empty when the tenant does not hold the backup.
    """

    physical_tenant_id: str
    state: ClusterHistoryBackupTenantState
    failure_reason: None | str
    details: list[HistoryBackupSnapshotInfo]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id = self.physical_tenant_id

        state = self.state.value

        failure_reason: None | str
        failure_reason = self.failure_reason

        details: list[dict[str, Any]] = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "state": state,
                "failureReason": failure_reason,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.history_backup_snapshot_info import HistoryBackupSnapshotInfo

        d = dict(src_dict)
        physical_tenant_id = d.pop("physicalTenantId")

        state = ClusterHistoryBackupTenantState(d.pop("state"))

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))

        details: list[HistoryBackupSnapshotInfo] = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = HistoryBackupSnapshotInfo.from_dict(details_item_data)

            details.append(details_item)

        cluster_history_backup_tenant_info = cls(
            physical_tenant_id=physical_tenant_id,
            state=state,
            failure_reason=failure_reason,
            details=details,
        )

        cluster_history_backup_tenant_info.additional_properties = d
        return cluster_history_backup_tenant_info

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
