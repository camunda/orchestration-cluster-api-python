from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import RoleId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="RoleSearchQueryRequestFilter")


@_attrs_define
class RoleSearchQueryRequestFilter:
    """The role search filters.

    Attributes:
        role_id (str | Unset): The role ID search filters. Example: admin.
        name (AdvancedStringFilter | str | Unset): The role name search filters.
    """

    role_id: RoleId | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        role_id = self.role_id

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role_id is not UNSET:
            field_dict["roleId"] = role_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)
        role_id = (
            RoleId(_val) if (_val := d.pop("roleId", UNSET)) is not UNSET else UNSET
        )

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

        role_search_query_request_filter = cls(
            role_id=role_id,
            name=name,
        )

        role_search_query_request_filter.additional_properties = d
        return role_search_query_request_filter

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
