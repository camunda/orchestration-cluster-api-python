from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    MessageKey,
    MessageSubscriptionKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_element_id,
    lift_element_instance_key,
    lift_message_key,
    lift_message_subscription_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CorrelatedMessageSubscriptionResult")


@_attrs_define
class CorrelatedMessageSubscriptionResult:
    """
    Attributes:
        correlation_key (None | str): The correlation key of the message.
        correlation_time (datetime.datetime): The time when the message was correlated.
        element_id (str): The element ID that received the message.
        element_instance_key (None | str): The element instance key that received the message.
            It is `null` for start event subscriptions.
             Example: 2251799813686789.
        message_key (str): The message key. Example: 2251799813683467.
        message_name (str): The name of the message.
        partition_id (int): The partition ID that correlated the message.
        process_definition_id (str): The process definition ID associated with this correlated message subscription.
            Example: new-account-onboarding-workflow.
        process_definition_key (str): The process definition key associated with this correlated message subscription.
            Example: 2251799813686749.
        process_instance_key (str): The process instance key associated with this correlated message subscription.
            Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        subscription_key (str): The subscription key that received the message. Example: 2251799813632456.
        tenant_id (str): The tenant ID associated with this correlated message subscription. Example: customer-service.
    """

    correlation_key: None | str
    correlation_time: datetime.datetime
    element_id: ElementId
    element_instance_key: None | ElementInstanceKey
    message_key: MessageKey
    message_name: str
    partition_id: int
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    subscription_key: MessageSubscriptionKey
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        correlation_key: None | str
        correlation_key = self.correlation_key

        correlation_time = self.correlation_time.isoformat()

        element_id = self.element_id

        element_instance_key: None | ElementInstanceKey
        element_instance_key = self.element_instance_key

        message_key = self.message_key

        message_name = self.message_name

        partition_id = self.partition_id

        process_definition_id = self.process_definition_id

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        subscription_key = self.subscription_key

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "correlationKey": correlation_key,
                "correlationTime": correlation_time,
                "elementId": element_id,
                "elementInstanceKey": element_instance_key,
                "messageKey": message_key,
                "messageName": message_name,
                "partitionId": partition_id,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "subscriptionKey": subscription_key,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_correlation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        correlation_key = _parse_correlation_key(d.pop("correlationKey"))

        correlation_time = isoparse(d.pop("correlationTime"))

        element_id = lift_element_id(d.pop("elementId"))

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey")
        )

        element_instance_key = (
            lift_element_instance_key(_raw_element_instance_key)
            if isinstance(_raw_element_instance_key, str)
            else _raw_element_instance_key
        )

        message_key = lift_message_key(d.pop("messageKey"))

        message_name = d.pop("messageName")

        partition_id = d.pop("partitionId")

        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            lift_process_instance_key(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        subscription_key = lift_message_subscription_key(d.pop("subscriptionKey"))

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        correlated_message_subscription_result = cls(
            correlation_key=correlation_key,
            correlation_time=correlation_time,
            element_id=element_id,
            element_instance_key=element_instance_key,
            message_key=message_key,
            message_name=message_name,
            partition_id=partition_id,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            subscription_key=subscription_key,
            tenant_id=tenant_id,
        )

        correlated_message_subscription_result.additional_properties = d
        return correlated_message_subscription_result

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
