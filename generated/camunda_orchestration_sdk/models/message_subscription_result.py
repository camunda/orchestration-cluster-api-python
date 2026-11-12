from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    MessageSubscriptionKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_subscription_state_enum import MessageSubscriptionStateEnum

T = TypeVar("T", bound="MessageSubscriptionResult")


@_attrs_define
class MessageSubscriptionResult:
    """
    Attributes:
        message_subscription_key (str): The message subscription key associated with this message subscription. Example:
            2251799813632456.
        process_definition_id (str): The process definition ID associated with this message subscription. Example: new-
            account-onboarding-workflow.
        process_definition_key (None | str): The process definition key associated with this message subscription.
            Example: 2251799813686749.
        process_instance_key (None | str): The process instance key associated with this message subscription. Example:
            2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        element_id (str): The element ID associated with this message subscription. Example: Activity_106kosb.
        element_instance_key (None | str): The element instance key associated with this message subscription. Example:
            2251799813686789.
        message_subscription_state (MessageSubscriptionStateEnum): The state of message subscription.
        last_updated_date (datetime.datetime): The last updated date of the message subscription.
        message_name (str): The name of the message associated with the message subscription.
        correlation_key (None | str): The correlation key of the message subscription.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    """

    message_subscription_key: MessageSubscriptionKey
    process_definition_id: ProcessDefinitionId
    process_definition_key: None | ProcessDefinitionKey
    process_instance_key: None | ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    element_id: ElementId
    element_instance_key: None | ElementInstanceKey
    message_subscription_state: MessageSubscriptionStateEnum
    last_updated_date: datetime.datetime
    message_name: str
    correlation_key: None | str
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        message_subscription_key = self.message_subscription_key

        process_definition_id = self.process_definition_id

        process_definition_key: None | ProcessDefinitionKey
        process_definition_key = self.process_definition_key

        process_instance_key: None | ProcessInstanceKey
        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        element_id = self.element_id

        element_instance_key: None | ElementInstanceKey
        element_instance_key = self.element_instance_key

        message_subscription_state = self.message_subscription_state.value

        last_updated_date = self.last_updated_date.isoformat()

        message_name = self.message_name

        correlation_key: None | str
        correlation_key = self.correlation_key

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messageSubscriptionKey": message_subscription_key,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "elementId": element_id,
                "elementInstanceKey": element_instance_key,
                "messageSubscriptionState": message_subscription_state,
                "lastUpdatedDate": last_updated_date,
                "messageName": message_name,
                "correlationKey": correlation_key,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message_subscription_key = MessageSubscriptionKey(
            d.pop("messageSubscriptionKey")
        )

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        def _parse_process_definition_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_definition_key = (
            ProcessDefinitionKey(_raw_process_definition_key)
            if isinstance(_raw_process_definition_key, str)
            else _raw_process_definition_key
        )

        def _parse_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey")
        )

        process_instance_key = (
            ProcessInstanceKey(_raw_process_instance_key)
            if isinstance(_raw_process_instance_key, str)
            else _raw_process_instance_key
        )

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        element_id = ElementId(d.pop("elementId"))

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey")
        )

        element_instance_key = (
            ElementInstanceKey(_raw_element_instance_key)
            if isinstance(_raw_element_instance_key, str)
            else _raw_element_instance_key
        )

        message_subscription_state = MessageSubscriptionStateEnum(
            d.pop("messageSubscriptionState")
        )

        last_updated_date = isoparse(d.pop("lastUpdatedDate"))

        message_name = d.pop("messageName")

        def _parse_correlation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        correlation_key = _parse_correlation_key(d.pop("correlationKey"))

        tenant_id = TenantId(d.pop("tenantId"))

        message_subscription_result = cls(
            message_subscription_key=message_subscription_key,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            element_id=element_id,
            element_instance_key=element_instance_key,
            message_subscription_state=message_subscription_state,
            last_updated_date=last_updated_date,
            message_name=message_name,
            correlation_key=correlation_key,
            tenant_id=tenant_id,
        )

        message_subscription_result.additional_properties = d
        return message_subscription_result

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
