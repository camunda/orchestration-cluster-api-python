from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.physical_tenant_broker_topology import PhysicalTenantBrokerTopology


T = TypeVar("T", bound="PhysicalTenantTopology")


@_attrs_define
class PhysicalTenantTopology:
    """The topology of a single physical tenant.

    Attributes:
        physical_tenant_id (str): The id of the physical tenant. Example: default.
        partitions_count (int): The number of partitions spread across this physical tenant. Example: 3.
        replication_factor (int): The configured replication factor for this physical tenant. Example: 3.
        last_completed_change_id (str): ID of the last completed change of this physical tenant. Example: -1.
        brokers (list[PhysicalTenantBrokerTopology]): The brokers holding partitions of this physical tenant.
    """

    physical_tenant_id: str
    partitions_count: int
    replication_factor: int
    last_completed_change_id: str
    brokers: list[PhysicalTenantBrokerTopology]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id = self.physical_tenant_id

        partitions_count = self.partitions_count

        replication_factor = self.replication_factor

        last_completed_change_id = self.last_completed_change_id

        brokers: list[dict[str, Any]] = []
        for brokers_item_data in self.brokers:
            brokers_item = brokers_item_data.to_dict()
            brokers.append(brokers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "partitionsCount": partitions_count,
                "replicationFactor": replication_factor,
                "lastCompletedChangeId": last_completed_change_id,
                "brokers": brokers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.physical_tenant_broker_topology import (
            PhysicalTenantBrokerTopology,
        )

        d = dict(src_dict)
        physical_tenant_id = d.pop("physicalTenantId")

        partitions_count = d.pop("partitionsCount")

        replication_factor = d.pop("replicationFactor")

        last_completed_change_id = d.pop("lastCompletedChangeId")

        brokers: list[PhysicalTenantBrokerTopology] = []
        _brokers = d.pop("brokers")
        for brokers_item_data in _brokers:
            brokers_item = PhysicalTenantBrokerTopology.from_dict(brokers_item_data)

            brokers.append(brokers_item)

        physical_tenant_topology = cls(
            physical_tenant_id=physical_tenant_id,
            partitions_count=partitions_count,
            replication_factor=replication_factor,
            last_completed_change_id=last_completed_change_id,
            brokers=brokers,
        )

        physical_tenant_topology.additional_properties = d
        return physical_tenant_topology

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
