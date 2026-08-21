from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_runtime_backup_tenant_state import (
        ClusterRuntimeBackupTenantState,
    )


T = TypeVar("T", bound="ClusterRuntimeBackupState")


@_attrs_define
class ClusterRuntimeBackupState:
    """The checkpoint and backup state of each physical tenant. Nothing is aggregated across tenants: checkpoint ids and
    log positions only mean anything within one tenant's partitions.

        Attributes:
            physical_tenants (list[ClusterRuntimeBackupTenantState]): The runtime backup state of each targeted physical
                tenant, ordered by physical tenant id.
    """

    physical_tenants: list[ClusterRuntimeBackupTenantState]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenants: list[dict[str, Any]] = []
        for physical_tenants_item_data in self.physical_tenants:
            physical_tenants_item = physical_tenants_item_data.to_dict()
            physical_tenants.append(physical_tenants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenants": physical_tenants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_runtime_backup_tenant_state import (
            ClusterRuntimeBackupTenantState,
        )

        d = dict(src_dict)
        physical_tenants: list[ClusterRuntimeBackupTenantState] = []
        _physical_tenants = d.pop("physicalTenants")
        for physical_tenants_item_data in _physical_tenants:
            physical_tenants_item = ClusterRuntimeBackupTenantState.from_dict(
                physical_tenants_item_data
            )

            physical_tenants.append(physical_tenants_item)

        cluster_runtime_backup_state = cls(
            physical_tenants=physical_tenants,
        )

        cluster_runtime_backup_state.additional_properties = d
        return cluster_runtime_backup_state

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
