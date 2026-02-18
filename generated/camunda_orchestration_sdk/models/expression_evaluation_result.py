from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExpressionEvaluationResult")


@_attrs_define
class ExpressionEvaluationResult:
    """
    Attributes:
        expression (str): The evaluated expression Example: =x + y.
        result (Any): The result value. Its type can vary. Example: 30.
        warnings (list[str]): List of warnings generated during expression evaluation
    """

    expression: str
    result: Any
    warnings: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        expression = self.expression

        result = self.result

        warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expression": expression,
                "result": result,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expression = d.pop("expression")

        result = d.pop("result")

        warnings = cast(list[str], d.pop("warnings"))

        expression_evaluation_result = cls(
            expression=expression,
            result=result,
            warnings=warnings,
        )

        expression_evaluation_result.additional_properties = d
        return expression_evaluation_result

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
