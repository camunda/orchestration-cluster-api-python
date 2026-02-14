from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="VariableValueFilterProperty")


@_attrs_define
class VariableValueFilterProperty:
    """
    Attributes:
        name (str): Name of the variable.
        value (AdvancedStringFilter | str):
    """

    name: str
    value: AdvancedStringFilter | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        name = self.name

        value: dict[str, Any] | str
        if isinstance(self.value, AdvancedStringFilter):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_value(data: object) -> AdvancedStringFilter | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                value_type_1 = AdvancedStringFilter.from_dict(data)

                return value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str, data)

        value = _parse_value(d.pop("value"))

        variable_value_filter_property = cls(
            name=name,
            value=value,
        )

        variable_value_filter_property.additional_properties = d
        return variable_value_filter_property

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
