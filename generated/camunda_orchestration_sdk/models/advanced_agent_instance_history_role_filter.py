from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.advanced_agent_instance_history_role_filter_eq import (
    AdvancedAgentInstanceHistoryRoleFilterEq,
)
from ..models.advanced_agent_instance_history_role_filter_neq import (
    AdvancedAgentInstanceHistoryRoleFilterNeq,
)
from ..models.agent_instance_history_role_enum import AgentInstanceHistoryRoleEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AdvancedAgentInstanceHistoryRoleFilter")


@_attrs_define
class AdvancedAgentInstanceHistoryRoleFilter:
    """Advanced AgentInstanceHistoryRoleEnum filter.

    Attributes:
        eq (AdvancedAgentInstanceHistoryRoleFilterEq | Unset): Checks for equality with the provided value.
        neq (AdvancedAgentInstanceHistoryRoleFilterNeq | Unset): Checks for inequality with the provided value.
        exists (bool | Unset): Checks if the current property exists.
        in_ (list[AgentInstanceHistoryRoleEnum] | Unset): Checks if the property matches any of the provided values.
    """

    eq: AdvancedAgentInstanceHistoryRoleFilterEq | Unset = UNSET
    neq: AdvancedAgentInstanceHistoryRoleFilterNeq | Unset = UNSET
    exists: bool | Unset = UNSET
    in_: list[AgentInstanceHistoryRoleEnum] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        eq: str | Unset = UNSET
        if not isinstance(self.eq, Unset):
            eq = self.eq.value

        neq: str | Unset = UNSET
        if not isinstance(self.neq, Unset):
            neq = self.neq.value

        exists = self.exists

        in_: list[str] | Unset = UNSET
        if not isinstance(self.in_, Unset):
            in_ = []
            for in_item_data in self.in_:
                in_item = in_item_data.value
                in_.append(in_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eq is not UNSET:
            field_dict["$eq"] = eq
        if neq is not UNSET:
            field_dict["$neq"] = neq
        if exists is not UNSET:
            field_dict["$exists"] = exists
        if in_ is not UNSET:
            field_dict["$in"] = in_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _eq = d.pop("$eq", UNSET)
        eq: AdvancedAgentInstanceHistoryRoleFilterEq | Unset
        if isinstance(_eq, Unset):
            eq = UNSET
        else:
            eq = AdvancedAgentInstanceHistoryRoleFilterEq(_eq)

        _neq = d.pop("$neq", UNSET)
        neq: AdvancedAgentInstanceHistoryRoleFilterNeq | Unset
        if isinstance(_neq, Unset):
            neq = UNSET
        else:
            neq = AdvancedAgentInstanceHistoryRoleFilterNeq(_neq)

        exists = d.pop("$exists", UNSET)

        _in_ = d.pop("$in", UNSET)
        in_: list[AgentInstanceHistoryRoleEnum] | Unset = UNSET
        if _in_ is not UNSET:
            in_ = []
            for in_item_data in _in_:
                in_item = AgentInstanceHistoryRoleEnum(in_item_data)

                in_.append(in_item)

        advanced_agent_instance_history_role_filter = cls(
            eq=eq,
            neq=neq,
            exists=exists,
            in_=in_,
        )

        advanced_agent_instance_history_role_filter.additional_properties = d
        return advanced_agent_instance_history_role_filter

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
