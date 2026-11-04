from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="UserTaskLookupRequest")


@_attrs_define
class UserTaskLookupRequest:
    """
    Attributes:
        fetch_variables (list[str] | Unset): The names of the variables to return. If absent or empty, all variables
            visible to the user task are returned. A name without a matching variable is left out of the response.
             Example: ['recommendation', 'applicant'].
    """

    fetch_variables: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        fetch_variables: list[str] | Unset = UNSET
        if not isinstance(self.fetch_variables, Unset):
            fetch_variables = self.fetch_variables

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fetch_variables is not UNSET:
            field_dict["fetchVariables"] = fetch_variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fetch_variables = cast(list[str], d.pop("fetchVariables", UNSET))

        user_task_lookup_request = cls(
            fetch_variables=fetch_variables,
        )

        user_task_lookup_request.additional_properties = d
        return user_task_lookup_request

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
