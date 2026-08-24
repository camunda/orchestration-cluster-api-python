from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, JobKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_instance_update_request_status import (
    AgentInstanceUpdateRequestStatus,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.agent_instance_history_item import AgentInstanceHistoryItem


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
        job_key (str): The key of the job activation during which this update is being made.
            An update must always be attributed to the active job that produced it.
             Example: 2251799813653498.
        job_lease (str): Opaque lease token received from the job activation response. Disambiguates
            this activation from any other activation of the same job: if the job is
            later retried, history items submitted under a superseded lease are discarded
            rather than committed.
        status (AgentInstanceUpdateRequestStatus | Unset): The new status of the agent instance.
        history (list[AgentInstanceHistoryItem] | None | Unset): A batch of history items to append to the agent
            instance's conversation
            history, in request order. Each created item is echoed back in the
            response's createdHistory, positionally correlated.
    """

    element_instance_key: ElementInstanceKey
    job_key: JobKey
    job_lease: str
    status: AgentInstanceUpdateRequestStatus | Unset = UNSET
    history: list[AgentInstanceHistoryItem] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_instance_key = self.element_instance_key

        job_key = self.job_key

        job_lease = self.job_lease

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

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
                "jobKey": job_key,
                "jobLease": job_lease,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if history is not UNSET:
            field_dict["history"] = history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_history_item import AgentInstanceHistoryItem

        d = dict(src_dict)
        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        job_key = JobKey(d.pop("jobKey"))

        job_lease = d.pop("jobLease")

        _status = d.pop("status", UNSET)
        status: AgentInstanceUpdateRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AgentInstanceUpdateRequestStatus(_status)

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

        agent_instance_update_request = cls(
            element_instance_key=element_instance_key,
            job_key=job_key,
            job_lease=job_lease,
            status=status,
            history=history,
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
