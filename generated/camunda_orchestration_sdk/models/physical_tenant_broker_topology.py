from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.partition import Partition


T = TypeVar("T", bound="PhysicalTenantBrokerTopology")


@_attrs_define
class PhysicalTenantBrokerTopology:
    """The partitions of one physical tenant that one broker manages or replicates.

    Attributes:
        broker_id (str): The unique (within a cluster) identifier of the broker, as reported in the cluster-level broker
            list.
             Example: eu-west-1_0.
        partitions (list[Partition]): The partitions of this physical tenant managed or replicated on this broker.
    """

    broker_id: str
    partitions: list[Partition]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        broker_id = self.broker_id

        partitions: list[dict[str, Any]] = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "brokerId": broker_id,
                "partitions": partitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partition import Partition

        d = dict(src_dict)
        broker_id = d.pop("brokerId")

        partitions: list[Partition] = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = Partition.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        physical_tenant_broker_topology = cls(
            broker_id=broker_id,
            partitions=partitions,
        )

        physical_tenant_broker_topology.additional_properties = d
        return physical_tenant_broker_topology

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
