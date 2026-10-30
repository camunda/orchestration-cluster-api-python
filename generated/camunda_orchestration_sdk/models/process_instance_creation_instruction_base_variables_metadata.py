from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.variable_metadata import VariableMetadata


T = TypeVar("T", bound="ProcessInstanceCreationInstructionBaseVariablesMetadata")


@_attrs_define
class ProcessInstanceCreationInstructionBaseVariablesMetadata:
    """Metadata of the variables, keyed by variable name. Use it to set how a variable is
    treated, for example to protect its value. A variable without an entry has no
    metadata.

    """

    additional_properties: dict[str, VariableMetadata] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.variable_metadata import VariableMetadata

        d = dict(src_dict)
        process_instance_creation_instruction_base_variables_metadata = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = VariableMetadata.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        process_instance_creation_instruction_base_variables_metadata.additional_properties = additional_properties
        return process_instance_creation_instruction_base_variables_metadata

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> VariableMetadata:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: VariableMetadata) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
