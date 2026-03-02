from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_element_id,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ProcessInstanceSequenceFlowResult")


@_attrs_define
class ProcessInstanceSequenceFlowResult:
    """Process instance sequence flow result.

    Attributes:
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        sequence_flow_id (str | Unset): The sequence flow id.
        process_instance_key (str | Unset): The key of this process instance. Example: 2251799813690746.
        process_definition_key (str | Unset): The process definition key. Example: 2251799813686749.
        process_definition_id (str | Unset): The process definition id. Example: new-account-onboarding-workflow.
        element_id (str | Unset): The element id for this sequence flow, as provided in the BPMN process. Example:
            Activity_106kosb.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
    """

    root_process_instance_key: None | ProcessInstanceKey
    sequence_flow_id: str | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        sequence_flow_id = self.sequence_flow_id

        process_instance_key = self.process_instance_key

        process_definition_key = self.process_definition_key

        process_definition_id = self.process_definition_id

        element_id = self.element_id

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rootProcessInstanceKey": root_process_instance_key,
            }
        )
        if sequence_flow_id is not UNSET:
            field_dict["sequenceFlowId"] = sequence_flow_id
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        sequence_flow_id = d.pop("sequenceFlowId", UNSET)

        process_instance_key = (
            lift_process_instance_key(_val)
            if (_val := d.pop("processInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_key = (
            lift_process_definition_key(_val)
            if (_val := d.pop("processDefinitionKey", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_id = (
            lift_process_definition_id(_val)
            if (_val := d.pop("processDefinitionId", UNSET)) is not UNSET
            else UNSET
        )

        element_id = (
            lift_element_id(_val)
            if (_val := d.pop("elementId", UNSET)) is not UNSET
            else UNSET
        )

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        process_instance_sequence_flow_result = cls(
            root_process_instance_key=root_process_instance_key,
            sequence_flow_id=sequence_flow_id,
            process_instance_key=process_instance_key,
            process_definition_key=process_definition_key,
            process_definition_id=process_definition_id,
            element_id=element_id,
            tenant_id=tenant_id,
        )

        process_instance_sequence_flow_result.additional_properties = d
        return process_instance_sequence_flow_result

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
