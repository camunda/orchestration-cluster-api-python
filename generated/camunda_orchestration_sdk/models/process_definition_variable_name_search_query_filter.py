from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="ProcessDefinitionVariableNameSearchQueryFilter")


@_attrs_define
class ProcessDefinitionVariableNameSearchQueryFilter:
    """The process definition variable name search filters.

    Attributes:
        name (AdvancedStringFilter | str | Unset): The variable name search filter.
    """

    name: AdvancedStringFilter | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = AdvancedStringFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        process_definition_variable_name_search_query_filter = cls(
            name=name,
        )

        return process_definition_variable_name_search_query_filter
