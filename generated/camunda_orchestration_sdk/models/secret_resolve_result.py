from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resolved_secret import ResolvedSecret
    from ..models.secret_resolution_error import SecretResolutionError


T = TypeVar("T", bound="SecretResolveResult")


@_attrs_define
class SecretResolveResult:
    """The per-reference outcome of a resolve request.

    Attributes:
        resolved (list[ResolvedSecret]): The references that were successfully resolved.
        errors (list[SecretResolutionError]): The references that could not be resolved, each with a typed error code.
    """

    resolved: list[ResolvedSecret]
    errors: list[SecretResolutionError]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        resolved: list[dict[str, Any]] = []
        for resolved_item_data in self.resolved:
            resolved_item = resolved_item_data.to_dict()
            resolved.append(resolved_item)

        errors: list[dict[str, Any]] = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resolved": resolved,
                "errors": errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_secret import ResolvedSecret
        from ..models.secret_resolution_error import SecretResolutionError

        d = dict(src_dict)
        resolved: list[ResolvedSecret] = []
        _resolved = d.pop("resolved")
        for resolved_item_data in _resolved:
            resolved_item = ResolvedSecret.from_dict(resolved_item_data)

            resolved.append(resolved_item)

        errors: list[SecretResolutionError] = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = SecretResolutionError.from_dict(errors_item_data)

            errors.append(errors_item)

        secret_resolve_result = cls(
            resolved=resolved,
            errors=errors,
        )

        secret_resolve_result.additional_properties = d
        return secret_resolve_result

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
