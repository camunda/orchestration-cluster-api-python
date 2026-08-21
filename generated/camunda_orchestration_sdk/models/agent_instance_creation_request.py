from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
    from ..models.agent_instance_history_item import AgentInstanceHistoryItem


T = TypeVar("T", bound="AgentInstanceCreationRequest")


@_attrs_define
class AgentInstanceCreationRequest:
    """Request to create a new agent instance.

    Attributes:
        element_instance_key (str): The key of the AI Agent Sub-process or AI Agent Task element instance.
            The engine uses this key to infer processInstanceKey, elementId,
            processDefinitionKey, and tenantId.
             Example: 2251799813686789.
        definition (AgentInstanceCreationRequestDefinition | Unset): The agent's initial definition; model, provider,
            and systemPrompt can
            all be changed later via a CONFIGURATION history item. Required when
            history is empty or omitted. Must be omitted when history is
            non-empty — supply model, provider, and systemPrompt through a
            CONFIGURATION item in history instead.
        limits (AgentInstanceCreationRequestLimits | Unset): Limits for the agent execution. When omitted, all limits
            default to -1
            (no limit). Must be omitted when history is non-empty — supply limits
            through a CONFIGURATION item in history instead, if needed.
        job_key (None | str | Unset): The key of the job activation during which this creation is being made.
            Required whenever history is non-empty.
             Example: 2251799813653498.
        job_lease (None | str | Unset): Opaque lease token received from the job activation response. Disambiguates
            this activation from any other activation of the same job: if the job is
            later retried, history items submitted under a superseded lease are discarded
            rather than committed.
        history (list[AgentInstanceHistoryItem] | None | Unset): A batch of history items to append to the agent
            instance's conversation
            history, in request order. Each created item is echoed back in the
            response's createdHistory, positionally correlated. When non-empty,
            model, provider, and systemPrompt (and, if needed, limits) must be
            established through a CONFIGURATION item in this batch instead of the
            top-level definition/limits, which must then be omitted.
    """

    element_instance_key: ElementInstanceKey
    definition: AgentInstanceCreationRequestDefinition | Unset = UNSET
    limits: AgentInstanceCreationRequestLimits | Unset = UNSET
    job_key: None | JobKey | Unset = UNSET
    job_lease: None | str | Unset = UNSET
    history: list[AgentInstanceHistoryItem] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_instance_key = self.element_instance_key

        definition: dict[str, Any] | Unset = UNSET
        if not isinstance(self.definition, Unset):
            definition = self.definition.to_dict()

        limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        job_key: None | JobKey | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        else:
            job_key = self.job_key

        job_lease: None | str | Unset
        if isinstance(self.job_lease, Unset):
            job_lease = UNSET
        else:
            job_lease = self.job_lease

        history: list[dict[str, Any]] | None | Unset
        if isinstance(self.history, Unset):
            history = UNSET
        elif isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)

        else:
            history = self.history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementInstanceKey": element_instance_key,
            }
        )
        if definition is not UNSET:
            field_dict["definition"] = definition
        if limits is not UNSET:
            field_dict["limits"] = limits
        if job_key is not UNSET:
            field_dict["jobKey"] = job_key
        if job_lease is not UNSET:
            field_dict["jobLease"] = job_lease
        if history is not UNSET:
            field_dict["history"] = history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_creation_request_definition import (
            AgentInstanceCreationRequestDefinition,
        )
        from ..models.agent_instance_creation_request_limits import (
            AgentInstanceCreationRequestLimits,
        )
        from ..models.agent_instance_history_item import AgentInstanceHistoryItem

        d = dict(src_dict)
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        _definition = d.pop("definition", UNSET)
        definition: AgentInstanceCreationRequestDefinition | Unset
        if isinstance(_definition, Unset):
            definition = UNSET
        else:
            definition = AgentInstanceCreationRequestDefinition.from_dict(_definition)

        _limits = d.pop("limits", UNSET)
        limits: AgentInstanceCreationRequestLimits | Unset
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = AgentInstanceCreationRequestLimits.from_dict(_limits)

        def _parse_job_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_job_key = _parse_job_key(d.pop("jobKey", UNSET))

        job_key = (
            JobKey(_raw_job_key) if isinstance(_raw_job_key, str) else _raw_job_key
        )

        def _parse_job_lease(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        job_lease = _parse_job_lease(d.pop("jobLease", UNSET))

        def _parse_history(
            data: object,
        ) -> list[AgentInstanceHistoryItem] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0: list[AgentInstanceHistoryItem] = []
                _history_type_0 = cast(list[Any], data)
                for history_type_0_item_data in _history_type_0:
                    history_type_0_item = AgentInstanceHistoryItem.from_dict(
                        history_type_0_item_data
                    )

                    history_type_0.append(history_type_0_item)

                return history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentInstanceHistoryItem] | None | Unset, data)

        history = _parse_history(d.pop("history", UNSET))

        agent_instance_creation_request = cls(
            element_instance_key=element_instance_key,
            definition=definition,
            limits=limits,
            job_key=job_key,
            job_lease=job_lease,
            history=history,
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
