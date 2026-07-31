from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_status_response_status import ClusterStatusResponseStatus

T = TypeVar("T", bound="ClusterStatusResponse")


@_attrs_define
class ClusterStatusResponse:
    """The aggregated status of the whole cluster.

    Attributes:
        status (ClusterStatusResponseStatus): `HEALTHY` when every physical tenant is healthy, `DOWN` when no physical
            tenant can process work, `DEGRADED` in every other case. Example: HEALTHY.
    """

    status: ClusterStatusResponseStatus
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ClusterStatusResponseStatus(d.pop("status"))

        cluster_status_response = cls(
            status=status,
        )

        cluster_status_response.additional_properties = d
        return cluster_status_response

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
