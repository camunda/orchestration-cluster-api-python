from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.agent_instance_creation_request_definition import (
        AgentInstanceCreationRequestDefinition,
    )
    from ..models.agent_instance_creation_request_limits import (
        AgentInstanceCreationRequestLimits,
    )


T = TypeVar("T", bound="AgentInstanceCreationRequest")


@_attrs_define
class AgentInstanceCreationRequest:
    """Request to create a new agent instance.

    Attributes:
        element_instance_key (str): The key of the AHSP or AI Agent Task element instance.
            The engine uses this key to infer processInstanceKey, elementId,
            processDefinitionKey, and tenantId.
             Example: 2251799813686789.
        definition (AgentInstanceCreationRequestDefinition): Static definition set once at creation.
        limits (AgentInstanceCreationRequestLimits | Unset): Limits for the agent execution. When omitted, all limits
            default to -1
            (no limit).
    """

    element_instance_key: ElementInstanceKey
    definition: AgentInstanceCreationRequestDefinition
    limits: AgentInstanceCreationRequestLimits | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_instance_key = self.element_instance_key

        definition = self.definition.to_dict()

        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementInstanceKey": element_instance_key,
                "definition": definition,
            }
        )
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_creation_request_definition import (
            AgentInstanceCreationRequestDefinition,
        )
        from ..models.agent_instance_creation_request_limits import (
            AgentInstanceCreationRequestLimits,
        )

        d = dict(src_dict)
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        definition = AgentInstanceCreationRequestDefinition.from_dict(
            d.pop("definition")
        )

        _limits = d.pop("limits", UNSET)
        limits: AgentInstanceCreationRequestLimits | Unset
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = AgentInstanceCreationRequestLimits.from_dict(_limits)

        agent_instance_creation_request = cls(
            element_instance_key=element_instance_key,
            definition=definition,
            limits=limits,
        )

        agent_instance_creation_request.additional_properties = d
        return agent_instance_creation_request

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
