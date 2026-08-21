from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_runtime_backup_tenant_state_state import (
        ClusterRuntimeBackupTenantStateState,
    )


T = TypeVar("T", bound="ClusterRuntimeBackupTenantState")


@_attrs_define
class ClusterRuntimeBackupTenantState:
    """The checkpoint and backup state of one physical tenant.

    Attributes:
        physical_tenant_id (str): The id of the physical tenant. Example: default.
        state (ClusterRuntimeBackupTenantStateState): The checkpoint and backup state of this physical tenant's
            partitions.
    """

    physical_tenant_id: str
    state: ClusterRuntimeBackupTenantStateState
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id = self.physical_tenant_id

        state = self.state.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_runtime_backup_tenant_state_state import (
            ClusterRuntimeBackupTenantStateState,
        )

        d = dict(src_dict)
        physical_tenant_id = d.pop("physicalTenantId")

        state = ClusterRuntimeBackupTenantStateState.from_dict(d.pop("state"))

        cluster_runtime_backup_tenant_state = cls(
            physical_tenant_id=physical_tenant_id,
            state=state,
        )

        cluster_runtime_backup_tenant_state.additional_properties = d
        return cluster_runtime_backup_tenant_state

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
