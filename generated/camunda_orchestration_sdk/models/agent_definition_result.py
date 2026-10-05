from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    AgentDefinitionKey,
    ElementId,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    TenantId,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.agent_definition_type_enum import AgentDefinitionTypeEnum

T = TypeVar("T", bound="AgentDefinitionResult")


@_attrs_define
class AgentDefinitionResult:
    """An agent definition, created at deploy time for the process element it belongs to.

    Attributes:
        agent_definition_key (str): The unique key for this agent definition. Unique across process definition versions.
             Example: 2251799813691958.
        agent_type (AgentDefinitionTypeEnum): The kind of agent an agent definition describes.
        name (str): The human-readable name of the process element that owns the agent definition. Falls
            back to elementId when the element has no BPMN name configured.
        element_id (str): The BPMN element ID of the process element that owns the agent definition. Example:
            Activity_106kosb.
        process_definition_id (str): The BPMN process ID of the process definition that owns the agent definition.
            Example: new-account-onboarding-workflow.
        process_definition_key (str): The key of the process definition that owns the agent definition. Example:
            2251799813686749.
        process_definition_version (int): The version of the process definition that owns the agent definition.
        process_definition_version_tag (None | str): The version tag of the process definition that owns the agent
            definition.
        tenant_id (str): The tenant ID of this agent definition. Example: customer-service.
    """

    agent_definition_key: AgentDefinitionKey
    agent_type: AgentDefinitionTypeEnum
    name: str
    element_id: ElementId
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_definition_version: int
    process_definition_version_tag: None | str
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        agent_definition_key = self.agent_definition_key

        agent_type = self.agent_type.value

        name = self.name

        element_id = self.element_id

        process_definition_id = self.process_definition_id

        process_definition_key = self.process_definition_key

        process_definition_version = self.process_definition_version

        process_definition_version_tag: None | str
        process_definition_version_tag = self.process_definition_version_tag

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agentDefinitionKey": agent_definition_key,
                "agentType": agent_type,
                "name": name,
                "elementId": element_id,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processDefinitionVersion": process_definition_version,
                "processDefinitionVersionTag": process_definition_version_tag,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_definition_key = AgentDefinitionKey(d.pop("agentDefinitionKey"))

        agent_type = AgentDefinitionTypeEnum(d.pop("agentType"))

        name = d.pop("name")

        element_id = ElementId(d.pop("elementId"))

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        process_definition_version = d.pop("processDefinitionVersion")

        def _parse_process_definition_version_tag(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        process_definition_version_tag = _parse_process_definition_version_tag(
            d.pop("processDefinitionVersionTag")
        )

        tenant_id = TenantId(d.pop("tenantId"))

        agent_definition_result = cls(
            agent_definition_key=agent_definition_key,
            agent_type=agent_type,
            name=name,
            element_id=element_id,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_definition_version=process_definition_version,
            process_definition_version_tag=process_definition_version_tag,
            tenant_id=tenant_id,
        )

        agent_definition_result.additional_properties = d
        return agent_definition_result

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
