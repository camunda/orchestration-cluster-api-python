from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="EvaluatedDecisionInputItem")


@_attrs_define
class EvaluatedDecisionInputItem:
    """A decision input that was evaluated within this decision evaluation.

    Attributes:
        input_id (str | Unset): The identifier of the decision input.
        input_name (str | Unset): The name of the decision input.
        input_value (str | Unset): The description of the decision input.
    """

    input_id: str | Unset = UNSET
    input_name: str | Unset = UNSET
    input_value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        input_id = self.input_id

        input_name = self.input_name

        input_value = self.input_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_id is not UNSET:
            field_dict["inputId"] = input_id
        if input_name is not UNSET:
            field_dict["inputName"] = input_name
        if input_value is not UNSET:
            field_dict["inputValue"] = input_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_id = d.pop("inputId", UNSET)

        input_name = d.pop("inputName", UNSET)

        input_value = d.pop("inputValue", UNSET)

        evaluated_decision_input_item = cls(
            input_id=input_id,
            input_name=input_name,
            input_value=input_value,
        )

        evaluated_decision_input_item.additional_properties = d
        return evaluated_decision_input_item

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
