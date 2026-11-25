from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.secret_status_exact_match import SecretStatusExactMatch
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.advanced_secret_status_filter import AdvancedSecretStatusFilter


T = TypeVar("T", bound="SecretListFilter")


@_attrs_define
class SecretListFilter:
    """Secret list filter.

    Attributes:
        status (AdvancedSecretStatusFilter | SecretStatusExactMatch | Unset): Only list secrets in the matching states.
            Omit it to list secrets in every state.
    """

    status: AdvancedSecretStatusFilter | SecretStatusExactMatch | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status: dict[str, Any] | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, SecretStatusExactMatch):
            status = self.status.value
        else:
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_secret_status_filter import (
            AdvancedSecretStatusFilter,  # noqa: PLC0415
        )

        d = dict(src_dict)

        def _parse_status(
            data: object,
        ) -> AdvancedSecretStatusFilter | SecretStatusExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = SecretStatusExactMatch(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            status_type_1 = AdvancedSecretStatusFilter.from_dict(data)

            return status_type_1

        status = _parse_status(d.pop("status", UNSET))

        secret_list_filter = cls(
            status=status,
        )

        return secret_list_filter
