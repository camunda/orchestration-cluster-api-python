from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.secret_list_request_filter import SecretListRequestFilter


T = TypeVar("T", bound="SecretListRequest")


@_attrs_define
class SecretListRequest:
    """Options for listing secrets. The request body is optional: omitting it, or sending an empty
    object, lists every secret the caller may read.

        Attributes:
            filter_ (SecretListRequestFilter | Unset): Narrows the listed secrets. Omit it to list secrets in every state.
                Clusters before 8.11
                reject this property with `400`.
    """

    filter_: SecretListRequestFilter | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.secret_list_request_filter import (
            SecretListRequestFilter,  # noqa: PLC0415
        )

        d = dict(src_dict)
        _filter_ = d.pop("filter", UNSET)
        filter_: SecretListRequestFilter | Unset
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = SecretListRequestFilter.from_dict(_filter_)

        secret_list_request = cls(
            filter_=filter_,
        )

        return secret_list_request
