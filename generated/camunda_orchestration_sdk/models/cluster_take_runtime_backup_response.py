from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_runtime_backup_take_result import (
        ClusterRuntimeBackupTakeResult,
    )


T = TypeVar("T", bound="ClusterTakeRuntimeBackupResponse")


@_attrs_define
class ClusterTakeRuntimeBackupResponse:
    """The outcome of triggering a runtime backup on every targeted physical tenant. Returned both when every tenant was
    triggered and when only some were, so a partial trigger is never silent: the status code says whether the request
    succeeded, the body says what is running.

        Attributes:
            physical_tenants (list[ClusterRuntimeBackupTakeResult]): The outcome for each targeted physical tenant, ordered
                by physical tenant id. Carries no cluster-level backup id: in generated-id mode each tenant generates its own.
    """

    physical_tenants: list[ClusterRuntimeBackupTakeResult]
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
        from ..models.cluster_runtime_backup_take_result import (
            ClusterRuntimeBackupTakeResult,
        )

        d = dict(src_dict)
        physical_tenants: list[ClusterRuntimeBackupTakeResult] = []
        _physical_tenants = d.pop("physicalTenants")
        for physical_tenants_item_data in _physical_tenants:
            physical_tenants_item = ClusterRuntimeBackupTakeResult.from_dict(
                physical_tenants_item_data
            )

            physical_tenants.append(physical_tenants_item)

        cluster_take_runtime_backup_response = cls(
            physical_tenants=physical_tenants,
        )

        cluster_take_runtime_backup_response.additional_properties = d
        return cluster_take_runtime_backup_response

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
