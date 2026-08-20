from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_history_backup_tenant_info import (
        ClusterHistoryBackupTenantInfo,
    )


T = TypeVar("T", bound="ClusterHistoryBackupInfo")


@_attrs_define
class ClusterHistoryBackupInfo:
    """A history backup id and what each physical tenant reports for it. No cluster-level state is aggregated from the per-
    tenant states.

        Attributes:
            backup_id (int): The id of the backup. Example: 1.
            physical_tenants (list[ClusterHistoryBackupTenantInfo]): What each physical tenant reports for this backup id,
                ordered by physical tenant id. When looking a backup id up directly, every targeted tenant is listed, including
                the ones reporting `NOT_FOUND`. Within a listing, only the tenants that hold the id are listed.
    """

    backup_id: int
    physical_tenants: list[ClusterHistoryBackupTenantInfo]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        physical_tenants: list[dict[str, Any]] = []
        for physical_tenants_item_data in self.physical_tenants:
            physical_tenants_item = physical_tenants_item_data.to_dict()
            physical_tenants.append(physical_tenants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backupId": backup_id,
                "physicalTenants": physical_tenants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_history_backup_tenant_info import (
            ClusterHistoryBackupTenantInfo,
        )

        d = dict(src_dict)
        backup_id = d.pop("backupId")

        physical_tenants: list[ClusterHistoryBackupTenantInfo] = []
        _physical_tenants = d.pop("physicalTenants")
        for physical_tenants_item_data in _physical_tenants:
            physical_tenants_item = ClusterHistoryBackupTenantInfo.from_dict(
                physical_tenants_item_data
            )

            physical_tenants.append(physical_tenants_item)

        cluster_history_backup_info = cls(
            backup_id=backup_id,
            physical_tenants=physical_tenants,
        )

        cluster_history_backup_info.additional_properties = d
        return cluster_history_backup_info

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
