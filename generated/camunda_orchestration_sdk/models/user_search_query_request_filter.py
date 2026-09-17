from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.user_filter_fields import UserFilterFields


T = TypeVar("T", bound="UserSearchQueryRequestFilter")


@_attrs_define
class UserSearchQueryRequestFilter:
    """The user search filters.

    Attributes:
        username (AdvancedStringFilter | str | Unset): The username of the user.
        name (AdvancedStringFilter | str | Unset): The name of the user.
        email (AdvancedStringFilter | str | Unset): The email of the user.
        or_ (list[UserFilterFields] | None | Unset): Defines a list of alternative filter groups combined using OR
            logic. Each object in the array is evaluated independently, and the filter matches if any one of them is
            satisfied.

            Top-level fields and the `$or` clause are combined using AND logic — meaning: (top-level filters) AND (any of
            the `$or` filters) must match.
            <br>
            <em>Example:</em>

            ```json
            {
              "$or": [
                { "username": "user-1" },
                { "username": "user-2" }
              ]
            }
            ```
            This matches users whose <code>username</code> is <em>user-1</em> or <em>user-2</em>.
            <br>
            <p>Note: Using complex <code>$or</code> conditions may impact performance, use with caution in high-volume
            environments.
    """

    username: AdvancedStringFilter | str | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    email: AdvancedStringFilter | str | Unset = UNSET
    or_: list[UserFilterFields] | None | Unset = UNSET
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

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        email: dict[str, Any] | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        elif isinstance(self.email, AdvancedStringFilter):
            email = self.email.to_dict()
        else:
            email = self.email

        or_: list[dict[str, Any]] | None | Unset
        if isinstance(self.or_, Unset):
            or_ = UNSET
        elif isinstance(self.or_, list):
            or_ = []
            for or_type_0_item_data in self.or_:
                or_type_0_item = or_type_0_item_data.to_dict()
                or_.append(or_type_0_item)

        else:
            or_ = self.or_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if name is not UNSET:
            field_dict["name"] = name
        if email is not UNSET:
            field_dict["email"] = email
        if or_ is not UNSET:
            field_dict["$or"] = or_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.user_filter_fields import UserFilterFields

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

        def _parse_email(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                email_type_1 = AdvancedStringFilter.from_dict(data)

                return email_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_or_(data: object) -> list[UserFilterFields] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                or_type_0: list[UserFilterFields] = []
                _or_type_0 = cast(list[Any], data)
                for or_type_0_item_data in _or_type_0:
                    or_type_0_item = UserFilterFields.from_dict(or_type_0_item_data)

                    or_type_0.append(or_type_0_item)

                return or_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UserFilterFields] | None | Unset, data)

        or_ = _parse_or_(d.pop("$or", UNSET))

        user_search_query_request_filter = cls(
            username=username,
            name=name,
            email=email,
            or_=or_,
        )

        user_search_query_request_filter.additional_properties = d
        return user_search_query_request_filter

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
