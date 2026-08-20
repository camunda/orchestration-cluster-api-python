from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClusterHistoryBackupTakeResult")


@_attrs_define
class ClusterHistoryBackupTakeResult:
    """The snapshots scheduled on a single physical tenant. Only successfully scheduled tenants are reported: the request
    fails as a whole if any targeted tenant could not schedule the backup.

        Attributes:
            physical_tenant_id (str): The id of the physical tenant. Example: default.
            scheduled_snapshots (list[str]): The names of the snapshots scheduled on this physical tenant.
    """

    physical_tenant_id: str
    scheduled_snapshots: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id = self.physical_tenant_id

        scheduled_snapshots = self.scheduled_snapshots

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "scheduledSnapshots": scheduled_snapshots,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        physical_tenant_id = d.pop("physicalTenantId")

        scheduled_snapshots = cast(list[str], d.pop("scheduledSnapshots"))

        cluster_history_backup_take_result = cls(
            physical_tenant_id=physical_tenant_id,
            scheduled_snapshots=scheduled_snapshots,
        )

        cluster_history_backup_take_result.additional_properties = d
        return cluster_history_backup_take_result

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
