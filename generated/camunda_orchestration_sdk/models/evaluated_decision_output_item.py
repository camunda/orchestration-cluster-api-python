from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="EvaluatedDecisionOutputItem")


@_attrs_define
class EvaluatedDecisionOutputItem:
    """The evaluated decision outputs.

    Attributes:
        rule_id (None | str): The ID of the matched rule.
        rule_index (int | None): The index of the matched rule.
        output_id (str | Unset): The ID of the evaluated decison output item.
        output_name (str | Unset): The name of the of the evaluated decison output item.
        output_value (str | Unset): The value of the evaluated decison output item.
    """

    rule_id: None | str
    rule_index: int | None
    output_id: str | Unset = UNSET
    output_name: str | Unset = UNSET
    output_value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        rule_id: None | str
        rule_id = self.rule_id

        rule_index: int | None
        rule_index = self.rule_index

        output_id = self.output_id

        output_name = self.output_name

        output_value = self.output_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ruleId": rule_id,
                "ruleIndex": rule_index,
            }
        )
        if output_id is not UNSET:
            field_dict["outputId"] = output_id
        if output_name is not UNSET:
            field_dict["outputName"] = output_name
        if output_value is not UNSET:
            field_dict["outputValue"] = output_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rule_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rule_id = _parse_rule_id(d.pop("ruleId"))

        def _parse_rule_index(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        rule_index = _parse_rule_index(d.pop("ruleIndex"))

        output_id = d.pop("outputId", UNSET)

        output_name = d.pop("outputName", UNSET)

        output_value = d.pop("outputValue", UNSET)

        evaluated_decision_output_item = cls(
            rule_id=rule_id,
            rule_index=rule_index,
            output_id=output_id,
            output_name=output_name,
            output_value=output_value,
        )

        evaluated_decision_output_item.additional_properties = d
        return evaluated_decision_output_item

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
