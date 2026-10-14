from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="RoleUserSearchQueryRequestFilter")


@_attrs_define
class RoleUserSearchQueryRequestFilter:
    """The user filter criteria.

    Attributes:
        username (AdvancedStringFilter | str | Unset): The username search filters.
    """

    username: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        username: dict[str, Any] | str | Unset
        if isinstance(self.username, Unset):
            username = UNSET
        elif isinstance(self.username, AdvancedStringFilter):
            username = self.username.to_dict()
        else:
            username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_username(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                username_type_1 = AdvancedStringFilter.from_dict(data)

                return username_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        username = _parse_username(d.pop("username", UNSET))

        role_user_search_query_request_filter = cls(
            username=username,
        )

        role_user_search_query_request_filter.additional_properties = d
        return role_user_search_query_request_filter

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
