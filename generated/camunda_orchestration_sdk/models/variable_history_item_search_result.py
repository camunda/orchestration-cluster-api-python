from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    ScopeKey,
    TenantId,
    VariableHistoryItemKey,
    VariableKey,
    lift_scope_key,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.variable_history_item_actor_type_enum import (
    VariableHistoryItemActorTypeEnum,
)
from ..models.variable_history_item_operation_type_enum import (
    VariableHistoryItemOperationTypeEnum,
)
from ..models.variable_history_item_variable_operation_type_enum import (
    VariableHistoryItemVariableOperationTypeEnum,
)

T = TypeVar("T", bound="VariableHistoryItemSearchResult")


@_attrs_define
class VariableHistoryItemSearchResult:
    """Variable history item search response item.

    Attributes:
        value (str): Value of this variable change. Can be truncated, also when `truncateValues` is false, for the
            output collection of a multi-instance element or an ad-hoc sub-process.
        is_truncated (bool): Indicates if the value is truncated.
        variable_history_item_key (str): The unique key of this variable history item. Example: 2251799813683999.
        variable_key (str): The key of the variable this history item belongs to. Example: 2251799813683287.
        name (str): Name of the variable.
        scope_key (str): The key of the scope where this variable is directly defined. For process-level
            variables, this is the process instance key. For local variables, this is the key
            of the specific element instance where the variable is directly defined.
        element_instance_key (None | str): The key of the element instance that caused this change, if any. Example:
            2251799813686789.
        element_id (None | str): The model-defined id of the element that caused this change, if any. Example:
            Activity_106kosb.
        process_instance_key (str): The key of the process instance of this variable. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        process_definition_key (str): The key of the process definition. Example: 2251799813686749.
        process_definition_id (str): The id of the process definition. Example: new-account-onboarding-workflow.
        tenant_id (str): The tenant id of this variable. Example: customer-service.
        timestamp (datetime.datetime): The timestamp when this change occurred.
        operation_type (VariableHistoryItemOperationTypeEnum): The type of operation that produced this variable change.
            Camunda can add values in later
            versions; clients must handle unknown values gracefully.
        variable_operation_type (VariableHistoryItemVariableOperationTypeEnum): What wrote this variable value, for
            example a job completion, a script result, or a
            multi-instance output collection. Camunda can add values in later versions; clients must
            handle unknown values gracefully.
        actor_type (VariableHistoryItemActorTypeEnum): The type of the actor who performed the operation. Camunda can
            add values in later
            versions; clients must handle unknown values gracefully.
        actor_id (None | str): The id of the user or client that caused this change, if known.
        agent_element_id (None | str): The element id of the agent that caused this change, for example the element id
            of an ad-hoc sub-process, if any.
             Example: Activity_106kosb.
    """

    value: str
    is_truncated: bool
    variable_history_item_key: VariableHistoryItemKey
    variable_key: VariableKey
    name: str
    scope_key: ScopeKey
    element_instance_key: None | ElementInstanceKey
    element_id: None | ElementId
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    process_definition_id: ProcessDefinitionId
    tenant_id: TenantId
    timestamp: datetime.datetime
    operation_type: VariableHistoryItemOperationTypeEnum
    variable_operation_type: VariableHistoryItemVariableOperationTypeEnum
    actor_type: VariableHistoryItemActorTypeEnum
    actor_id: None | str
    agent_element_id: None | ElementId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        is_truncated = self.is_truncated

        variable_history_item_key = self.variable_history_item_key

        variable_key = self.variable_key

        name = self.name

        scope_key: ScopeKey
        scope_key = self.scope_key

        element_instance_key: None | ElementInstanceKey
        element_instance_key = self.element_instance_key

        element_id: None | ElementId
        element_id = self.element_id

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_definition_key = self.process_definition_key

        process_definition_id = self.process_definition_id

        tenant_id = self.tenant_id

        timestamp = self.timestamp.isoformat()

        operation_type = self.operation_type.value

        variable_operation_type = self.variable_operation_type.value

        actor_type = self.actor_type.value

        actor_id: None | str
        actor_id = self.actor_id

        agent_element_id: None | ElementId
        agent_element_id = self.agent_element_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "isTruncated": is_truncated,
                "variableHistoryItemKey": variable_history_item_key,
                "variableKey": variable_key,
                "name": name,
                "scopeKey": scope_key,
                "elementInstanceKey": element_instance_key,
                "elementId": element_id,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "processDefinitionKey": process_definition_key,
                "processDefinitionId": process_definition_id,
                "tenantId": tenant_id,
                "timestamp": timestamp,
                "operationType": operation_type,
                "variableOperationType": variable_operation_type,
                "actorType": actor_type,
                "actorId": actor_id,
                "agentElementId": agent_element_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        value = d.pop_required("value")

        is_truncated = d.pop_required("isTruncated")

        variable_history_item_key = VariableHistoryItemKey(
            d.pop_required("variableHistoryItemKey")
        )

        variable_key = VariableKey(d.pop_required("variableKey"))

        name = d.pop_required("name")

        def _parse_scope_key(data: object) -> str:
            return cast(str, data)

        _raw_scope_key = _parse_scope_key(d.pop_required("scopeKey"))

        scope_key = lift_scope_key(_raw_scope_key)

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(
            d.pop_required("elementInstanceKey")
        )

        element_instance_key = (
            ElementInstanceKey(_raw_element_instance_key)
            if isinstance(_raw_element_instance_key, str)
            else _raw_element_instance_key
        )

        def _parse_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_id = _parse_element_id(d.pop_required("elementId"))

        element_id = (
            ElementId(_raw_element_id)
            if isinstance(_raw_element_id, str)
            else _raw_element_id
        )

        process_instance_key = ProcessInstanceKey(d.pop_required("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop_required("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        process_definition_key = ProcessDefinitionKey(
            d.pop_required("processDefinitionKey")
        )

        process_definition_id = ProcessDefinitionId(
            d.pop_required("processDefinitionId")
        )

        tenant_id = TenantId(d.pop_required("tenantId"))

        timestamp = isoparse(d.pop_required("timestamp"))

        operation_type = VariableHistoryItemOperationTypeEnum(
            d.pop_required("operationType")
        )

        variable_operation_type = VariableHistoryItemVariableOperationTypeEnum(
            d.pop_required("variableOperationType")
        )

        actor_type = VariableHistoryItemActorTypeEnum(d.pop_required("actorType"))

        def _parse_actor_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_id = _parse_actor_id(d.pop_required("actorId"))

        def _parse_agent_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_agent_element_id = _parse_agent_element_id(
            d.pop_required("agentElementId")
        )

        agent_element_id = (
            ElementId(_raw_agent_element_id)
            if isinstance(_raw_agent_element_id, str)
            else _raw_agent_element_id
        )

        variable_history_item_search_result = cls(
            value=value,
            is_truncated=is_truncated,
            variable_history_item_key=variable_history_item_key,
            variable_key=variable_key,
            name=name,
            scope_key=scope_key,
            element_instance_key=element_instance_key,
            element_id=element_id,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            process_definition_key=process_definition_key,
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
            timestamp=timestamp,
            operation_type=operation_type,
            variable_operation_type=variable_operation_type,
            actor_type=actor_type,
            actor_id=actor_id,
            agent_element_id=agent_element_id,
        )

        variable_history_item_search_result.additional_properties = d
        return variable_history_item_search_result

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
