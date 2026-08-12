from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.agent_definition_type_exact_match import AgentDefinitionTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_agent_definition_key_filter import (
    AdvancedAgentDefinitionKeyFilter,
)
from ..models.advanced_agent_definition_type_filter import (
    AdvancedAgentDefinitionTypeFilter,
)
from ..models.advanced_element_id_filter import AdvancedElementIdFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_process_definition_id_filter import (
    AdvancedProcessDefinitionIdFilter,
)
from ..models.advanced_process_definition_key_filter import (
    AdvancedProcessDefinitionKeyFilter,
)
from ..models.advanced_string_filter import AdvancedStringFilter

T = TypeVar("T", bound="AgentDefinitionFilter")

@_attrs_define
class AgentDefinitionFilter:
    agent_definition_key: AdvancedAgentDefinitionKeyFilter | str | Unset = UNSET
    agent_type: (
        AdvancedAgentDefinitionTypeFilter | AgentDefinitionTypeExactMatch | Unset
    ) = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    process_definition_id: AdvancedProcessDefinitionIdFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_definition_version: AdvancedIntegerFilter | int | Unset = UNSET
    process_definition_version_tag: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
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
