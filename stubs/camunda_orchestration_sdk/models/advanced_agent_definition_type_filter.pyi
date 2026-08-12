from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.advanced_agent_definition_type_filter_eq import (
    AdvancedAgentDefinitionTypeFilterEq,
)
from ..models.advanced_agent_definition_type_filter_neq import (
    AdvancedAgentDefinitionTypeFilterNeq,
)
from ..models.agent_definition_type_enum import AgentDefinitionTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedAgentDefinitionTypeFilter")

@_attrs_define
class AdvancedAgentDefinitionTypeFilter:
    eq: AdvancedAgentDefinitionTypeFilterEq | Unset = UNSET
    neq: AdvancedAgentDefinitionTypeFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[AgentDefinitionTypeEnum] | Unset = UNSET
    not_in: list[AgentDefinitionTypeEnum] | Unset = UNSET
    like: str | Unset = UNSET
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
