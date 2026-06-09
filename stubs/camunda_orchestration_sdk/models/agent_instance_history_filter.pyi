from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.agent_instance_history_commit_status_exact_match import (
    AgentInstanceHistoryCommitStatusExactMatch,
)
from ..models.agent_instance_history_role_exact_match import (
    AgentInstanceHistoryRoleExactMatch,
)
from ..types import UNSET, Unset, str_any_dict_factory
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

T = TypeVar("T", bound="AgentInstanceHistoryFilter")

@_attrs_define
class AgentInstanceHistoryFilter:
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
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
