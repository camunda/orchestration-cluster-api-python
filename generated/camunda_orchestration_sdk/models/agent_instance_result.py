from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import AgentInstanceKey, ElementId, ProcessDefinitionKey, ProcessInstanceKey, TenantId

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_status_enum import AgentInstanceStatusEnum

if TYPE_CHECKING:
    from ..models.agent_instance_result_definition import AgentInstanceResultDefinition
    from ..models.agent_instance_result_limits import AgentInstanceResultLimits
    from ..models.agent_instance_result_metrics import AgentInstanceResultMetrics


T = TypeVar("T", bound="AgentInstanceResult")


@_attrs_define
class AgentInstanceResult:
    """
    Attributes:
        agent_instance_key (str): The unique key for this agent instance. Example: 4503599627370496.
        status (AgentInstanceStatusEnum): The current status of an agent instance.
        definition (AgentInstanceResultDefinition): The static definition of the agent, including model, provider, and
            system prompt.
        metrics (AgentInstanceResultMetrics): Aggregated metrics across all iterations of this agent instance.
        limits (AgentInstanceResultLimits): The configured limits for this agent instance, set once at creation.
        element_id (str): The BPMN element ID of the ad-hoc sub-process or AI agent task that owns this agent instance.
            Example: Activity_106kosb.
        process_instance_key (str): The key of the process instance that owns this agent instance. Example:
            2251799813690746.
        process_definition_key (str): The key of the process definition associated with this agent instance. Example:
            2251799813686749.
        tenant_id (str): The tenant ID of this agent instance. Example: customer-service.
        creation_date (datetime.datetime): The date when this agent instance was created.
        last_updated_date (datetime.datetime): The date when this agent instance was last updated.
        completion_date (datetime.datetime | None): The date when this agent instance completed. Null while the agent is
            still running.
    """

    agent_instance_key: AgentInstanceKey
    status: AgentInstanceStatusEnum
    definition: AgentInstanceResultDefinition
    metrics: AgentInstanceResultMetrics
    limits: AgentInstanceResultLimits
    element_id: ElementId
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    tenant_id: TenantId
    creation_date: datetime.datetime
    last_updated_date: datetime.datetime
    completion_date: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        agent_instance_key = self.agent_instance_key

        status = self.status.value

        definition = self.definition.to_dict()

        metrics = self.metrics.to_dict()

        limits = self.limits.to_dict()

        element_id = self.element_id

        process_instance_key = self.process_instance_key

        process_definition_key = self.process_definition_key

        tenant_id = self.tenant_id

        creation_date = self.creation_date.isoformat()

        last_updated_date = self.last_updated_date.isoformat()

        completion_date: None | str
        if isinstance(self.completion_date, datetime.datetime):
            completion_date = self.completion_date.isoformat()
        else:
            completion_date = self.completion_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agentInstanceKey": agent_instance_key,
                "status": status,
                "definition": definition,
                "metrics": metrics,
                "limits": limits,
                "elementId": element_id,
                "processInstanceKey": process_instance_key,
                "processDefinitionKey": process_definition_key,
                "tenantId": tenant_id,
                "creationDate": creation_date,
                "lastUpdatedDate": last_updated_date,
                "completionDate": completion_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_result_definition import (
            AgentInstanceResultDefinition,
        )
        from ..models.agent_instance_result_limits import AgentInstanceResultLimits
        from ..models.agent_instance_result_metrics import AgentInstanceResultMetrics

        d = dict(src_dict)
        agent_instance_key = AgentInstanceKey(d.pop("agentInstanceKey"))

        status = AgentInstanceStatusEnum(d.pop("status"))

        definition = AgentInstanceResultDefinition.from_dict(d.pop("definition"))

        metrics = AgentInstanceResultMetrics.from_dict(d.pop("metrics"))

        limits = AgentInstanceResultLimits.from_dict(d.pop("limits"))

        element_id = ElementId(d.pop("elementId"))

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        tenant_id = TenantId(d.pop("tenantId"))

        creation_date = isoparse(d.pop("creationDate"))

        last_updated_date = isoparse(d.pop("lastUpdatedDate"))

        def _parse_completion_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completion_date_type_0 = isoparse(data)

                return completion_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completion_date = _parse_completion_date(d.pop("completionDate"))

        agent_instance_result = cls(
            agent_instance_key=agent_instance_key,
            status=status,
            definition=definition,
            metrics=metrics,
            limits=limits,
            element_id=element_id,
            process_instance_key=process_instance_key,
            process_definition_key=process_definition_key,
            tenant_id=tenant_id,
            creation_date=creation_date,
            last_updated_date=last_updated_date,
            completion_date=completion_date,
        )

        agent_instance_result.additional_properties = d
        return agent_instance_result

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
