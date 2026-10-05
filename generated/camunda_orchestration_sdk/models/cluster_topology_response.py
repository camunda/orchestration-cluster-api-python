from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_broker_info import ClusterBrokerInfo
    from ..models.physical_tenant_topology import PhysicalTenantTopology


T = TypeVar("T", bound="ClusterTopologyResponse")


@_attrs_define
class ClusterTopologyResponse:
    """The topology of the whole cluster, aggregated over all physical tenants.

    Attributes:
        brokers (list[ClusterBrokerInfo]): The brokers that are part of this cluster, across all physical tenants.
        cluster_id (None | str): The cluster Id.
        cluster_size (int): The number of brokers in the cluster. Example: 3.
        gateway_version (None | str): The version of the Orchestration Cluster Gateway. Example: 8.10.0.
        physical_tenants (list[PhysicalTenantTopology]): The topology of each physical tenant of this cluster.
    """

    brokers: list[ClusterBrokerInfo]
    cluster_id: None | str
    cluster_size: int
    gateway_version: None | str
    physical_tenants: list[PhysicalTenantTopology]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        brokers: list[dict[str, Any]] = []
        for brokers_item_data in self.brokers:
            brokers_item = brokers_item_data.to_dict()
            brokers.append(brokers_item)

        cluster_id: None | str
        cluster_id = self.cluster_id

        cluster_size = self.cluster_size

        gateway_version: None | str
        gateway_version = self.gateway_version

        physical_tenants: list[dict[str, Any]] = []
        for physical_tenants_item_data in self.physical_tenants:
            physical_tenants_item = physical_tenants_item_data.to_dict()
            physical_tenants.append(physical_tenants_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "brokers": brokers,
                "clusterId": cluster_id,
                "clusterSize": cluster_size,
                "gatewayVersion": gateway_version,
                "physicalTenants": physical_tenants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_broker_info import ClusterBrokerInfo
        from ..models.physical_tenant_topology import PhysicalTenantTopology

        d = dict(src_dict)
        brokers: list[ClusterBrokerInfo] = []
        _brokers = d.pop("brokers")
        for brokers_item_data in _brokers:
            brokers_item = ClusterBrokerInfo.from_dict(brokers_item_data)

            brokers.append(brokers_item)

        def _parse_cluster_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cluster_id = _parse_cluster_id(d.pop("clusterId"))

        cluster_size = d.pop("clusterSize")

        def _parse_gateway_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gateway_version = _parse_gateway_version(d.pop("gatewayVersion"))

        physical_tenants: list[PhysicalTenantTopology] = []
        _physical_tenants = d.pop("physicalTenants")
        for physical_tenants_item_data in _physical_tenants:
            physical_tenants_item = PhysicalTenantTopology.from_dict(
                physical_tenants_item_data
            )

            physical_tenants.append(physical_tenants_item)

        cluster_topology_response = cls(
            brokers=brokers,
            cluster_id=cluster_id,
            cluster_size=cluster_size,
            gateway_version=gateway_version,
            physical_tenants=physical_tenants,
        )

        cluster_topology_response.additional_properties = d
        return cluster_topology_response

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
