from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.modify_process_instance_variable_instruction_variables import (
        ModifyProcessInstanceVariableInstructionVariables,
    )


T = TypeVar("T", bound="ModifyProcessInstanceVariableInstruction")


@_attrs_define
class ModifyProcessInstanceVariableInstruction:
    """Instruction describing which variables to create or update.

    Attributes:
        variables (ModifyProcessInstanceVariableInstructionVariables): JSON document that will instantiate the variables
            at the scope defined by the scopeId.
            It must be a JSON object, as variables will be mapped in a key-value fashion.
        scope_id (str | Unset): The id of the element in which scope the variables should be created.
            Leave empty to create the variables in the global scope of the process instance.
             Default: ''.
    """

    variables: ModifyProcessInstanceVariableInstructionVariables
    scope_id: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        variables = self.variables.to_dict()

        scope_id = self.scope_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "variables": variables,
            }
        )
        if scope_id is not UNSET:
            field_dict["scopeId"] = scope_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.modify_process_instance_variable_instruction_variables import (
            ModifyProcessInstanceVariableInstructionVariables,
        )

        d = dict(src_dict)
        variables = ModifyProcessInstanceVariableInstructionVariables.from_dict(
            d.pop("variables")
        )

        scope_id = d.pop("scopeId", UNSET)

        modify_process_instance_variable_instruction = cls(
            variables=variables,
            scope_id=scope_id,
        )

        modify_process_instance_variable_instruction.additional_properties = d
        return modify_process_instance_variable_instruction

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
