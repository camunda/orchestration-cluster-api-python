from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
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
        job_key (str): The key of the job activation during which this creation is being made.
            A creation must always be attributed to the active job that produced it.
             Example: 2251799813653498.
        job_lease (str): Opaque lease token received from the job activation response. Disambiguates
            this activation from any other activation of the same job: if the job is
            later retried, history items submitted under a superseded lease are discarded
            rather than committed.
        history (list[AgentInstanceHistoryItem]): A batch of history items to append to the agent instance's
            conversation
            history, in request order. Each created item is echoed back in the
            response's createdHistory, positionally correlated. Must include a
            CONFIGURATION item establishing model, provider, and systemPrompt (and,
            if needed, limits).
    """

    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    history: list[AgentInstanceHistoryItem]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_instance_key = self.element_instance_key

        job_key = self.job_key

        job_lease = self.job_lease

        history: list[dict[str, Any]] = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
                "jobLease": job_lease,
                "history": history,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_history_item import AgentInstanceHistoryItem

        d = dict(src_dict)
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        job_key = JobKey(d.pop("jobKey"))

        job_lease = d.pop("jobLease")

        history: list[AgentInstanceHistoryItem] = []
        _history = d.pop("history")
        for history_item_data in _history:
            history_item = AgentInstanceHistoryItem.from_dict(history_item_data)

            history.append(history_item)

        agent_instance_creation_request = cls(
            element_instance_key=element_instance_key,
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
