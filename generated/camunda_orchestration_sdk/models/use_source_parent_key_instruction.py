from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="UseSourceParentKeyInstruction")


@_attrs_define
class UseSourceParentKeyInstruction:
    """Instructs the engine to use the source's direct parent key as the ancestor scope key for the target element. This is
    a simpler alternative to `inferred` that skips hierarchy traversal and directly uses the source's parent key. This
    is useful when the source and target elements are siblings within the same flow scope.

        Attributes:
            ancestor_scope_type (str): The type of ancestor scope instruction. Example: sourceParent.
    """

    ancestor_scope_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        ancestor_scope_type = self.ancestor_scope_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ancestorScopeType": ancestor_scope_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ancestor_scope_type = d.pop("ancestorScopeType")

        use_source_parent_key_instruction = cls(
            ancestor_scope_type=ancestor_scope_type,
        )

        use_source_parent_key_instruction.additional_properties = d
        return use_source_parent_key_instruction

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
