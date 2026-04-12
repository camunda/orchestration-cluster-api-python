from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionId,
    ProcessDefinitionKey,
    TenantId,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProcessDefinitionMessageSubscriptionStatisticsResult")


@_attrs_define
class ProcessDefinitionMessageSubscriptionStatisticsResult:
    """
    Attributes:
        process_definition_id (str): The process definition ID associated with this message subscription. Example: new-
            account-onboarding-workflow.
        tenant_id (str): The tenant ID associated with this message subscription. Example: customer-service.
        process_definition_key (str): The process definition key associated with this message subscription. Example:
            2251799813686749.
        process_instances_with_active_subscriptions (int): The number of process instances with active message
            subscriptions.
        active_subscriptions (int): The total number of active message subscriptions for this process definition key.
    """

    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId
    process_definition_key: ProcessDefinitionKey
    process_instances_with_active_subscriptions: int
    active_subscriptions: int
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        tenant_id = self.tenant_id

        process_definition_key = self.process_definition_key

        process_instances_with_active_subscriptions = (
            self.process_instances_with_active_subscriptions
        )

        active_subscriptions = self.active_subscriptions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "tenantId": tenant_id,
                "processDefinitionKey": process_definition_key,
                "processInstancesWithActiveSubscriptions": process_instances_with_active_subscriptions,
                "activeSubscriptions": active_subscriptions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        tenant_id = TenantId(d.pop("tenantId"))

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        process_instances_with_active_subscriptions = d.pop(
            "processInstancesWithActiveSubscriptions"
        )

        active_subscriptions = d.pop("activeSubscriptions")

        process_definition_message_subscription_statistics_result = cls(
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
            process_definition_key=process_definition_key,
            process_instances_with_active_subscriptions=process_instances_with_active_subscriptions,
            active_subscriptions=active_subscriptions,
        )

        process_definition_message_subscription_statistics_result.additional_properties = d
        return process_definition_message_subscription_statistics_result

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
