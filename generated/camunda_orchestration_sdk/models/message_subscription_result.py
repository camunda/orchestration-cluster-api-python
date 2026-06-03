from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, MessageSubscriptionKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_subscription_state_enum import MessageSubscriptionStateEnum
from ..models.message_subscription_type_enum import MessageSubscriptionTypeEnum

if TYPE_CHECKING:
    from ..models.message_subscription_result_tool_properties import (
        MessageSubscriptionResultToolProperties,
    )


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
        process_instance_key (None | str): The process instance key associated with this message subscription.
            Only populated for intermediate event entities.
             Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        element_id (str): The element ID associated with this message subscription. Example: Activity_106kosb.
        element_instance_key (None | str): The element instance key associated with this message subscription.
            Only populated for intermediate event entities.
             Example: 2251799813686789.
        message_subscription_state (MessageSubscriptionStateEnum): The state of message subscription.
        last_updated_date (datetime.datetime): The last updated date of the message subscription.
        message_name (str): The name of the message associated with the message subscription.
        correlation_key (None | str): The correlation key of the message subscription.
        message_subscription_type (MessageSubscriptionTypeEnum): The type of message subscription.
            `START_EVENT` is definition-scoped (process start events). Always has a value; only
            captured from Camunda 8.10 onwards.
            `PROCESS_EVENT` is instance-scoped (intermediate catch events). Pre-8.10 entries have
            no value stored; the API returns `PROCESS_EVENT` as a default for those entries.
        tool_properties (MessageSubscriptionResultToolProperties): The subset of `zeebe:properties` extension properties
            whose keys start with the
            `io.camunda.tool:` prefix, extracted from the BPMN element associated with this
            subscription. Empty object when no matching properties are defined.
        process_definition_name (None | str): The name of the process definition associated with this message
            subscription.
        process_definition_version (int | None): The version of the process definition associated with this message
            subscription.
        tool_name (None | str): Tool name extracted from the `io.camunda.tool:name` zeebe:property.
            Null when the property is absent.
        inbound_connector_type (None | str): Inbound connector type extracted from the `inbound.type` zeebe:property.
            Null when the property is absent.
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
    message_subscription_type: MessageSubscriptionTypeEnum
    tool_properties: MessageSubscriptionResultToolProperties
    process_definition_name: None | str
    process_definition_version: int | None
    tool_name: None | str
    inbound_connector_type: None | str
    tenant_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

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

        message_subscription_type = self.message_subscription_type.value

        tool_properties = self.tool_properties.to_dict()

        process_definition_name: None | str
        process_definition_name = self.process_definition_name

        process_definition_version: int | None
        process_definition_version = self.process_definition_version

        tool_name: None | str
        tool_name = self.tool_name

        inbound_connector_type: None | str
        inbound_connector_type = self.inbound_connector_type

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
                "messageSubscriptionType": message_subscription_type,
                "toolProperties": tool_properties,
                "processDefinitionName": process_definition_name,
                "processDefinitionVersion": process_definition_version,
                "toolName": tool_name,
                "inboundConnectorType": inbound_connector_type,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_subscription_result_tool_properties import (
            MessageSubscriptionResultToolProperties,
        )

        d = dict(src_dict)
        message_subscription_key = MessageSubscriptionKey(d.pop("messageSubscriptionKey"))

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        def _parse_process_definition_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey")
        )


        process_definition_key = ProcessDefinitionKey(_raw_process_definition_key) if isinstance(_raw_process_definition_key, str) else _raw_process_definition_key

        def _parse_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_instance_key = _parse_process_instance_key(d.pop("processInstanceKey"))


        process_instance_key = ProcessInstanceKey(_raw_process_instance_key) if isinstance(_raw_process_instance_key, str) else _raw_process_instance_key

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )


        root_process_instance_key = ProcessInstanceKey(_raw_root_process_instance_key) if isinstance(_raw_root_process_instance_key, str) else _raw_root_process_instance_key

        element_id = ElementId(d.pop("elementId"))

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(d.pop("elementInstanceKey"))


        element_instance_key = ElementInstanceKey(_raw_element_instance_key) if isinstance(_raw_element_instance_key, str) else _raw_element_instance_key

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

        message_subscription_type = MessageSubscriptionTypeEnum(
            d.pop("messageSubscriptionType")
        )

        tool_properties = MessageSubscriptionResultToolProperties.from_dict(
            d.pop("toolProperties")
        )

        def _parse_process_definition_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        process_definition_name = _parse_process_definition_name(
            d.pop("processDefinitionName")
        )

        def _parse_process_definition_version(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        process_definition_version = _parse_process_definition_version(
            d.pop("processDefinitionVersion")
        )

        def _parse_tool_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tool_name = _parse_tool_name(d.pop("toolName"))

        def _parse_inbound_connector_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        inbound_connector_type = _parse_inbound_connector_type(
            d.pop("inboundConnectorType")
        )

        tenant_id = d.pop("tenantId")

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
            message_subscription_type=message_subscription_type,
            tool_properties=tool_properties,
            process_definition_name=process_definition_name,
            process_definition_version=process_definition_version,
            tool_name=tool_name,
            inbound_connector_type=inbound_connector_type,
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
