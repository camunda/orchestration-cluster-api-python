from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_runtime_backup_info_runtime_backup_state import (
    ClusterRuntimeBackupInfoRuntimeBackupState,
)

if TYPE_CHECKING:
    from ..models.cluster_runtime_backup_tenant_info import (
        ClusterRuntimeBackupTenantInfo,
    )


T = TypeVar("T", bound="ClusterRuntimeBackupInfo")


@_attrs_define
class ClusterRuntimeBackupInfo:
    """A runtime backup id, what each physical tenant reports for it, and the state aggregated over every targeted tenant —
    folded from the per-tenant states by the same rules a per-tenant state is folded from its partitions.

        Attributes:
            backup_id (int): The id of the backup. Example: 1.
            state (ClusterRuntimeBackupInfoRuntimeBackupState): The state aggregated over every targeted physical tenant,
                whether the backup id was looked up directly or listed. A tenant holding nothing for this id counts as
                `DOES_NOT_EXIST`, so the aggregate is `INCOMPLETE` unless every targeted tenant holds the backup. Example:
                IN_PROGRESS.
            failure_reason (None | str): Reason for failure if the aggregated state is 'FAILED'.
            physical_tenants (list[ClusterRuntimeBackupTenantInfo]): What each physical tenant reports for this backup id,
                ordered by physical tenant id. Every targeted tenant is listed, including the ones reporting `DOES_NOT_EXIST`.
    """

    backup_id: int
    state: ClusterRuntimeBackupInfoRuntimeBackupState
    failure_reason: None | str
    physical_tenants: list[ClusterRuntimeBackupTenantInfo]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        state = self.state.value

        failure_reason: None | str
        failure_reason = self.failure_reason

        physical_tenants: list[dict[str, Any]] = []
        for physical_tenants_item_data in self.physical_tenants:
            physical_tenants_item = physical_tenants_item_data.to_dict()
            physical_tenants.append(physical_tenants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backupId": backup_id,
                "state": state,
                "failureReason": failure_reason,
                "physicalTenants": physical_tenants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_runtime_backup_tenant_info import (
            ClusterRuntimeBackupTenantInfo,
        )

        d = dict(src_dict)
        backup_id = d.pop("backupId")

        state = ClusterRuntimeBackupInfoRuntimeBackupState(d.pop("state"))

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))

        physical_tenants: list[ClusterRuntimeBackupTenantInfo] = []
        _physical_tenants = d.pop("physicalTenants")
        for physical_tenants_item_data in _physical_tenants:
            physical_tenants_item = ClusterRuntimeBackupTenantInfo.from_dict(
                physical_tenants_item_data
            )

            physical_tenants.append(physical_tenants_item)

        cluster_runtime_backup_info = cls(
            backup_id=backup_id,
            state=state,
            failure_reason=failure_reason,
            physical_tenants=physical_tenants,
        )

        cluster_runtime_backup_info.additional_properties = d
        return cluster_runtime_backup_info

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
