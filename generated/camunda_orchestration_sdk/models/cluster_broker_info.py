from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClusterBrokerInfo")


@_attrs_define
class ClusterBrokerInfo:
    """Provides information on a broker node, independent of any physical tenant.

    Attributes:
        broker_id (str): The unique (within a cluster) broker identifier. When the cluster is not zoned, then it's a
            string that represents the nodeId (an integer). When the cluster is zoned, instead, it's of the form
            "$zoneName_$nodeId", providing uniqueness even across zones.
             Example: eu-west-1_0.
        host (str): The hostname for reaching the broker. Example: zeebe-0.zeebe-broker-service.
        port (int): The port for reaching the broker. Example: 26501.
        version (str): The broker version. Example: 8.10.0.
    """

    broker_id: str
    host: str
    port: int
    version: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        broker_id = self.broker_id

        host = self.host

        port = self.port

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "brokerId": broker_id,
                "host": host,
                "port": port,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        broker_id = d.pop("brokerId")

        host = d.pop("host")

        port = d.pop("port")

        version = d.pop("version")

        cluster_broker_info = cls(
            broker_id=broker_id,
            host=host,
            port=port,
            version=version,
        )

        cluster_broker_info.additional_properties = d
        return cluster_broker_info

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
