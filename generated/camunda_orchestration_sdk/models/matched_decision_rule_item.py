from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.evaluated_decision_output_item import EvaluatedDecisionOutputItem


T = TypeVar("T", bound="MatchedDecisionRuleItem")


@_attrs_define
class MatchedDecisionRuleItem:
    """A decision rule that matched within this decision evaluation.

    Attributes:
        evaluated_outputs (list[EvaluatedDecisionOutputItem]): The evaluated decision outputs.
        rule_id (str | Unset): The ID of the matched rule.
        rule_index (int | Unset): The index of the matched rule.
    """

    evaluated_outputs: list[EvaluatedDecisionOutputItem]
    rule_id: str | Unset = UNSET
    rule_index: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        evaluated_outputs: list[dict[str, Any]] = []
        for evaluated_outputs_item_data in self.evaluated_outputs:
            evaluated_outputs_item = evaluated_outputs_item_data.to_dict()
            evaluated_outputs.append(evaluated_outputs_item)

        rule_id = self.rule_id

        rule_index = self.rule_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "evaluatedOutputs": evaluated_outputs,
            }
        )
        if rule_id is not UNSET:
            field_dict["ruleId"] = rule_id
        if rule_index is not UNSET:
            field_dict["ruleIndex"] = rule_index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluated_decision_output_item import EvaluatedDecisionOutputItem

        d = dict(src_dict)
        evaluated_outputs: list[EvaluatedDecisionOutputItem] = []
        _evaluated_outputs = d.pop("evaluatedOutputs")
        for evaluated_outputs_item_data in _evaluated_outputs:
            evaluated_outputs_item = EvaluatedDecisionOutputItem.from_dict(
                evaluated_outputs_item_data
            )

            evaluated_outputs.append(evaluated_outputs_item)

        rule_id = d.pop("ruleId", UNSET)

        rule_index = d.pop("ruleIndex", UNSET)

        matched_decision_rule_item = cls(
            evaluated_outputs=evaluated_outputs,
            rule_id=rule_id,
            rule_index=rule_index,
        )

        matched_decision_rule_item.additional_properties = d
        return matched_decision_rule_item

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
