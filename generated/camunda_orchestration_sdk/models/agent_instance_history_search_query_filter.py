from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_history_commit_status_exact_match import (
    AgentInstanceHistoryCommitStatusExactMatch,
)
from ..models.agent_instance_history_role_exact_match import (
    AgentInstanceHistoryRoleExactMatch,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_agent_history_item_key_filter import (
        AdvancedAgentHistoryItemKeyFilter,
    )
    from ..models.advanced_agent_instance_history_commit_status_filter import (
        AdvancedAgentInstanceHistoryCommitStatusFilter,
    )
    from ..models.advanced_agent_instance_history_role_filter import (
        AdvancedAgentInstanceHistoryRoleFilter,
    )
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_job_key_filter import AdvancedJobKeyFilter


T = TypeVar("T", bound="AgentInstanceHistorySearchQueryFilter")


@_attrs_define
class AgentInstanceHistorySearchQueryFilter:
    """The history item search filters.

    Attributes:
        history_item_key (AdvancedAgentHistoryItemKeyFilter | str | Unset): The unique key of the history item.
        role (AdvancedAgentInstanceHistoryRoleFilter | AgentInstanceHistoryRoleExactMatch | Unset): The role of the
            history item.
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset): The key of the element instance under
            which the history item was produced.
        job_key (AdvancedJobKeyFilter | str | Unset): The key of the job activation that produced the history item.
        iteration (AdvancedIntegerFilter | int | Unset): The iteration number.
        commit_status (AdvancedAgentInstanceHistoryCommitStatusFilter | AgentInstanceHistoryCommitStatusExactMatch |
            Unset): The commit status of the history item. Defaults to COMMITTED only.
            Include PENDING or DISCARDED explicitly to debug in-flight or failed activations.
        produced_at (AdvancedDateTimeFilter | datetime.datetime | Unset): The timestamp when the history item was
            produced.
    """

    history_item_key: AdvancedAgentHistoryItemKeyFilter | str | Unset = UNSET
    role: (
        AdvancedAgentInstanceHistoryRoleFilter
        | AgentInstanceHistoryRoleExactMatch
        | Unset
    ) = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    job_key: AdvancedJobKeyFilter | str | Unset = UNSET
    iteration: AdvancedIntegerFilter | int | Unset = UNSET
    commit_status: (
        AdvancedAgentInstanceHistoryCommitStatusFilter
        | AgentInstanceHistoryCommitStatusExactMatch
        | Unset
    ) = UNSET
    produced_at: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_agent_history_item_key_filter import (
            AdvancedAgentHistoryItemKeyFilter,
        )
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter

        history_item_key: dict[str, Any] | str | Unset
        if isinstance(self.history_item_key, Unset):
            history_item_key = UNSET
        elif isinstance(self.history_item_key, AdvancedAgentHistoryItemKeyFilter):
            history_item_key = self.history_item_key.to_dict()
        else:
            history_item_key = self.history_item_key

        role: dict[str, Any] | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        elif isinstance(self.role, AgentInstanceHistoryRoleExactMatch):
            role = self.role.value
        else:
            role = self.role.to_dict()

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, AdvancedElementInstanceKeyFilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        job_key: dict[str, Any] | str | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        elif isinstance(self.job_key, AdvancedJobKeyFilter):
            job_key = self.job_key.to_dict()
        else:
            job_key = self.job_key

        iteration: dict[str, Any] | int | Unset
        if isinstance(self.iteration, Unset):
            iteration = UNSET
        elif isinstance(self.iteration, AdvancedIntegerFilter):
            iteration = self.iteration.to_dict()
        else:
            iteration = self.iteration

        commit_status: dict[str, Any] | str | Unset
        if isinstance(self.commit_status, Unset):
            commit_status = UNSET
        elif isinstance(self.commit_status, AgentInstanceHistoryCommitStatusExactMatch):
            commit_status = self.commit_status.value
        else:
            commit_status = self.commit_status.to_dict()

        produced_at: dict[str, Any] | str | Unset
        if isinstance(self.produced_at, Unset):
            produced_at = UNSET
        elif isinstance(self.produced_at, datetime.datetime):
            produced_at = self.produced_at.isoformat()
        else:
            produced_at = self.produced_at.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if history_item_key is not UNSET:
            field_dict["historyItemKey"] = history_item_key
        if role is not UNSET:
            field_dict["role"] = role
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if job_key is not UNSET:
            field_dict["jobKey"] = job_key
        if iteration is not UNSET:
            field_dict["iteration"] = iteration
        if commit_status is not UNSET:
            field_dict["commitStatus"] = commit_status
        if produced_at is not UNSET:
            field_dict["producedAt"] = produced_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_agent_history_item_key_filter import (
            AdvancedAgentHistoryItemKeyFilter,
        )
        from ..models.advanced_agent_instance_history_commit_status_filter import (
            AdvancedAgentInstanceHistoryCommitStatusFilter,
        )
        from ..models.advanced_agent_instance_history_role_filter import (
            AdvancedAgentInstanceHistoryRoleFilter,
        )
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter

        d = dict(src_dict)

        def _parse_history_item_key(
            data: object,
        ) -> AdvancedAgentHistoryItemKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                history_item_key_type_1 = AdvancedAgentHistoryItemKeyFilter.from_dict(
                    data
                )

                return history_item_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAgentHistoryItemKeyFilter | str | Unset, data)

        history_item_key = _parse_history_item_key(d.pop("historyItemKey", UNSET))

        def _parse_role(
            data: object,
        ) -> (
            AdvancedAgentInstanceHistoryRoleFilter
            | AgentInstanceHistoryRoleExactMatch
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = AgentInstanceHistoryRoleExactMatch(data)

                return role_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            role_type_1 = AdvancedAgentInstanceHistoryRoleFilter.from_dict(data)

            return role_type_1

        role = _parse_role(d.pop("role", UNSET))

        def _parse_element_instance_key(
            data: object,
        ) -> AdvancedElementInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_instance_key_type_1 = (
                    AdvancedElementInstanceKeyFilter.from_dict(data)
                )

                return element_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementInstanceKeyFilter | str | Unset, data)

        element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey", UNSET)
        )

        def _parse_job_key(data: object) -> AdvancedJobKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                job_key_type_1 = AdvancedJobKeyFilter.from_dict(data)

                return job_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedJobKeyFilter | str | Unset, data)

        job_key = _parse_job_key(d.pop("jobKey", UNSET))

        def _parse_iteration(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                iteration_type_1 = AdvancedIntegerFilter.from_dict(data)

                return iteration_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        iteration = _parse_iteration(d.pop("iteration", UNSET))

        def _parse_commit_status(
            data: object,
        ) -> (
            AdvancedAgentInstanceHistoryCommitStatusFilter
            | AgentInstanceHistoryCommitStatusExactMatch
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                commit_status_type_0 = AgentInstanceHistoryCommitStatusExactMatch(data)

                return commit_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            commit_status_type_1 = (
                AdvancedAgentInstanceHistoryCommitStatusFilter.from_dict(data)
            )

            return commit_status_type_1

        commit_status = _parse_commit_status(d.pop("commitStatus", UNSET))

        def _parse_produced_at(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                produced_at_type_0 = isoparse(data)

                return produced_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            produced_at_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return produced_at_type_1

        produced_at = _parse_produced_at(d.pop("producedAt", UNSET))

        agent_instance_history_search_query_filter = cls(
            history_item_key=history_item_key,
            role=role,
            element_instance_key=element_instance_key,
            job_key=job_key,
            iteration=iteration,
            commit_status=commit_status,
            produced_at=produced_at,
        )

        agent_instance_history_search_query_filter.additional_properties = d
        return agent_instance_history_search_query_filter

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
