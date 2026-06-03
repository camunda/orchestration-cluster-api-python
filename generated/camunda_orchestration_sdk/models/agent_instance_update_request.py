from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_instance_update_request_status import (
    AgentInstanceUpdateRequestStatus,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.agent_instance_update_request_metrics import (
        AgentInstanceUpdateRequestMetrics,
    )
    from ..models.agent_tool import AgentTool


T = TypeVar("T", bound="AgentInstanceUpdateRequest")


@_attrs_define
class AgentInstanceUpdateRequest:
    """Request to update the mutable state of an agent instance.

    Attributes:
        element_instance_key (str): The key of the currently-active element instance for this agent instance.
            Used for ownership/equality validation against the stored agent instance
            and, when the supplied key differs from the previous association (re-entry
            of an ad-hoc sub-process or AI Agent task), appended to elementInstanceKeys
            with the reverse link updated on the supplied element instance.
             Example: 2251799813686789.
        status (AgentInstanceUpdateRequestStatus | Unset): The new status of the agent instance.
        metrics (AgentInstanceUpdateRequestMetrics | Unset): Metric increments to apply to the aggregate counters.
        tools (list[AgentTool] | None | Unset): The complete list of tools available to the agent, replacing any
            previously
            stored tools. When provided, the engine replaces the existing tool list with
            this value.
    """

    element_instance_key: ElementInstanceKey
    status: AgentInstanceUpdateRequestStatus | Unset = UNSET
    metrics: AgentInstanceUpdateRequestMetrics | Unset = UNSET
    tools: list[AgentTool] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        element_instance_key = self.element_instance_key

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementInstanceKey": element_instance_key,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_update_request_metrics import (
            AgentInstanceUpdateRequestMetrics,
        )
        from ..models.agent_tool import AgentTool

        d = dict(src_dict)
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        _status = d.pop("status", UNSET)
        status: AgentInstanceUpdateRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AgentInstanceUpdateRequestStatus(_status)

        _metrics = d.pop("metrics", UNSET)
        metrics: AgentInstanceUpdateRequestMetrics | Unset
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = AgentInstanceUpdateRequestMetrics.from_dict(_metrics)

        def _parse_tools(data: object) -> list[AgentTool] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0: list[AgentTool] = []
                _tools_type_0 = cast(list[Any], data)
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = AgentTool.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentTool] | None | Unset, data)

        tools = _parse_tools(d.pop("tools", UNSET))

        agent_instance_update_request = cls(
            element_instance_key=element_instance_key,
            status=status,
            metrics=metrics,
            tools=tools,
        )

        agent_instance_update_request.additional_properties = d
        return agent_instance_update_request

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
