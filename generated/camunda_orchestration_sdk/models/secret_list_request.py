from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SecretListRequest")


@_attrs_define
class SecretListRequest:
    """Reserved for future filtering options. Currently takes no properties. The request body is
    optional: omitting it (or sending an empty object) applies no filters.

    """

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        secret_list_request = cls()

        return secret_list_request
