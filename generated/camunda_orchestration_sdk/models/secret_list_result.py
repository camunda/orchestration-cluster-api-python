from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecretListResult")


@_attrs_define
class SecretListResult:
    """The secret references the caller is authorized to see.

    Unbounded for now: Phase 1's backend is mocked with at most 3 references. Pagination is
    expected to land here before GA, once a real secret store can return a tenant's full
    enumeration in one response. This is an alpha endpoint, so that is not yet a
    breaking-contract concern.

        Attributes:
            references (list[str]): The secret references, each of the form `camunda.secrets.<name>`.
    """

    references: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        references = self.references

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "references": references,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        references = cast(list[str], d.pop("references"))

        secret_list_result = cls(
            references=references,
        )

        secret_list_result.additional_properties = d
        return secret_list_result

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
