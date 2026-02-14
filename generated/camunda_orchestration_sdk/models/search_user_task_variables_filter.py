from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.name_advanced_filter import NameAdvancedFilter


T = TypeVar("T", bound="SearchUserTaskVariablesFilter")


@_attrs_define
class SearchUserTaskVariablesFilter:
    """The user task variable search filters.

    Attributes:
        name (NameAdvancedFilter | str | Unset):
    """

    name: NameAdvancedFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.name_advanced_filter import NameAdvancedFilter

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, NameAdvancedFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name_advanced_filter import NameAdvancedFilter

        d = dict(src_dict)

        def _parse_name(data: object) -> NameAdvancedFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = NameAdvancedFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(NameAdvancedFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        search_user_task_variables_filter = cls(
            name=name,
        )

        search_user_task_variables_filter.additional_properties = d
        return search_user_task_variables_filter

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
