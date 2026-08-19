from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExpressionSecretReferenceItem")


@_attrs_define
class ExpressionSecretReferenceItem:
    """
    Attributes:
        store_id (str): The identifier of the secret store that holds the referenced secret Example: default.
        secret_name (str): The secret name, e.g. "token" for "camunda.secrets.token" Example: token.
    """

    store_id: str
    secret_name: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        store_id = self.store_id

        secret_name = self.secret_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "storeId": store_id,
                "secretName": secret_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        store_id = d.pop("storeId")

        secret_name = d.pop("secretName")

        expression_secret_reference_item = cls(
            store_id=store_id,
            secret_name=secret_name,
        )

        expression_secret_reference_item.additional_properties = d
        return expression_secret_reference_item

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
