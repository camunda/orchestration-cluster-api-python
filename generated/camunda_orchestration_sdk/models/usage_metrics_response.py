from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.usage_metrics_response_tenants import UsageMetricsResponseTenants


T = TypeVar("T", bound="UsageMetricsResponse")


@_attrs_define
class UsageMetricsResponse:
    """
    Attributes:
        active_tenants (int): The amount of active tenants.
        tenants (UsageMetricsResponseTenants): The usage metrics by tenants. Only available if request `withTenants`
            query parameter was `true`.
        process_instances (int): The amount of created root process instances.
        decision_instances (int): The amount of executed decision instances.
        assignees (int): The amount of unique active task users.
    """

    active_tenants: int
    tenants: UsageMetricsResponseTenants
    process_instances: int
    decision_instances: int
    assignees: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        active_tenants = self.active_tenants

        tenants = self.tenants.to_dict()

        process_instances = self.process_instances

        decision_instances = self.decision_instances

        assignees = self.assignees

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activeTenants": active_tenants,
                "tenants": tenants,
                "processInstances": process_instances,
                "decisionInstances": decision_instances,
                "assignees": assignees,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_metrics_response_tenants import UsageMetricsResponseTenants

        d = dict(src_dict)
        active_tenants = d.pop("activeTenants")

        tenants = UsageMetricsResponseTenants.from_dict(d.pop("tenants"))

        process_instances = d.pop("processInstances")

        decision_instances = d.pop("decisionInstances")

        assignees = d.pop("assignees")

        usage_metrics_response = cls(
            active_tenants=active_tenants,
            tenants=tenants,
            process_instances=process_instances,
            decision_instances=decision_instances,
            assignees=assignees,
        )

        usage_metrics_response.additional_properties = d
        return usage_metrics_response

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
