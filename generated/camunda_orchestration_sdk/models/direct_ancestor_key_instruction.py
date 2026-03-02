from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementInstanceKey,
    lift_element_instance_key,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DirectAncestorKeyInstruction")


@_attrs_define
class DirectAncestorKeyInstruction:
    """Provides a concrete key to use as ancestor scope for the created element instance.

    Attributes:
        ancestor_scope_type (str): The type of ancestor scope instruction. Example: direct.
        ancestor_element_instance_key (str): System-generated key for a element instance. Example: 2251799813686789.
    """

    ancestor_scope_type: str
    ancestor_element_instance_key: ElementInstanceKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        ancestor_scope_type = self.ancestor_scope_type

        ancestor_element_instance_key = self.ancestor_element_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ancestorScopeType": ancestor_scope_type,
                "ancestorElementInstanceKey": ancestor_element_instance_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ancestor_scope_type = d.pop("ancestorScopeType")

        ancestor_element_instance_key = lift_element_instance_key(
            d.pop("ancestorElementInstanceKey")
        )

        direct_ancestor_key_instruction = cls(
            ancestor_scope_type=ancestor_scope_type,
            ancestor_element_instance_key=ancestor_element_instance_key,
        )

        direct_ancestor_key_instruction.additional_properties = d
        return direct_ancestor_key_instruction

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
