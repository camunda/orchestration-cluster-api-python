from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

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
    """Request to update the mutable state of an agent instance. At least one of
    status, metrics, or tools must be provided.

        Attributes:
            status (AgentInstanceUpdateRequestStatus | Unset): The new status of the agent instance.
            metrics (AgentInstanceUpdateRequestMetrics | Unset): Metric increments to apply to the aggregate counters.
            tools (list[AgentTool] | Unset): The complete list of tools available to the agent, replacing any previously
                stored tools. When provided, the engine replaces the existing tool list with
                this value.
    """

    status: AgentInstanceUpdateRequestStatus | Unset = UNSET
    metrics: AgentInstanceUpdateRequestMetrics | Unset = UNSET
    tools: list[AgentTool] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()
                tools.append(tools_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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

        _tools = d.pop("tools", UNSET)
        tools: list[AgentTool] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = AgentTool.from_dict(tools_item_data)

                tools.append(tools_item)

        agent_instance_update_request = cls(
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
