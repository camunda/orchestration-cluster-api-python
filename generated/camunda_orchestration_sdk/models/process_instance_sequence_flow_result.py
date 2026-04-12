from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProcessInstanceSequenceFlowResult")


@_attrs_define
class ProcessInstanceSequenceFlowResult:
    """Process instance sequence flow result.

    Attributes:
        sequence_flow_id (str): The sequence flow id.
        process_instance_key (str): The key of this process instance. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        process_definition_key (str): The process definition key. Example: 2251799813686749.
        process_definition_id (str): The process definition id. Example: new-account-onboarding-workflow.
        element_id (str): The element id for this sequence flow, as provided in the BPMN process. Example:
            Activity_106kosb.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    """

    sequence_flow_id: str
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    process_definition_id: ProcessDefinitionId
    element_id: ElementId
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        sequence_flow_id = self.sequence_flow_id

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_definition_key = self.process_definition_key

        process_definition_id = self.process_definition_id

        element_id = self.element_id

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sequenceFlowId": sequence_flow_id,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "processDefinitionKey": process_definition_key,
                "processDefinitionId": process_definition_id,
                "elementId": element_id,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sequence_flow_id = d.pop("sequenceFlowId")

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

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

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        element_id = ElementId(d.pop("elementId"))

        tenant_id = TenantId(d.pop("tenantId"))

        process_instance_sequence_flow_result = cls(
            sequence_flow_id=sequence_flow_id,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
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
