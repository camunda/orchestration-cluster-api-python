from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.group_filter_fields import GroupFilterFields


T = TypeVar("T", bound="GroupSearchQueryRequestFilter")


@_attrs_define
class GroupSearchQueryRequestFilter:
    """The group search filters.

    Attributes:
        group_id (AdvancedStringFilter | str | Unset): The group ID search filters.
        name (AdvancedStringFilter | str | Unset): The group name search filters.
        or_ (list[GroupFilterFields] | Unset): Defines a list of alternative filter groups combined using OR logic. Each
            object in the array is evaluated independently, and the filter matches if any one of them is satisfied.

            Top-level fields and the `$or` clause are combined using AND logic — meaning: (top-level filters) AND (any of
            the `$or` filters) must match.
            <br>
            <em>Example:</em>

            ```json
            {
              "$or": [
                { "groupId": "group-1" },
                { "groupId": "group-2" }
              ]
            }
            ```
            This matches groups whose <code>groupId</code> is <em>group-1</em> or <em>group-2</em>.
            <br>
            <p>Note: Using complex <code>$or</code> conditions may impact performance, use with caution in high-volume
            environments.
    """

    group_id: AdvancedStringFilter | str | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    or_: list[GroupFilterFields] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        group_id: dict[str, Any] | str | Unset
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        elif isinstance(self.group_id, AdvancedStringFilter):
            group_id = self.group_id.to_dict()
        else:
            group_id = self.group_id

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        or_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.or_, Unset):
            or_ = []
            for or_item_data in self.or_:
                or_item = or_item_data.to_dict()
                or_.append(or_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if group_id is not UNSET:
            field_dict["groupId"] = group_id
        if name is not UNSET:
            field_dict["name"] = name
        if or_ is not UNSET:
            field_dict["$or"] = or_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.group_filter_fields import GroupFilterFields

        d = dict(src_dict)

        def _parse_group_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                group_id_type_1 = AdvancedStringFilter.from_dict(data)

                return group_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        group_id = _parse_group_id(d.pop("groupId", UNSET))

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

        _or_ = d.pop("$or", UNSET)
        or_: list[GroupFilterFields] | Unset = UNSET
        if _or_ is not UNSET:
            or_ = []
            for or_item_data in _or_:
                or_item = GroupFilterFields.from_dict(or_item_data)

                or_.append(or_item)

        group_search_query_request_filter = cls(
            group_id=group_id,
            name=name,
            or_=or_,
        )

        group_search_query_request_filter.additional_properties = d
        return group_search_query_request_filter

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
