from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.secret_error_code import SecretErrorCode

T = TypeVar("T", bound="SecretResolutionError")


@_attrs_define
class SecretResolutionError:
    """
    Attributes:
        reference (str): The secret reference that could not be resolved.
        code (SecretErrorCode): The typed reason a reference could not be resolved.

            - `NOT_FOUND`: no secret exists for the reference.
            - `ACCESS_DENIED`: the caller lacks `SECRET:REVEAL` on the reference.
            - `INVALID_REFERENCE`: the reference is malformed, or the configured store rejected it as
              an invalid secret identifier.
            - `UNREADABLE`: the configured store could not return a value for the reference, for
              example because it rejected the cluster's own store credentials or the stored value could
              not be read. Whether the secret exists is not implied.
        message (str): A human-readable description of the failure. Never contains the secret value;
            only error metadata (codes, names) is included.
    """

    reference: str
    code: SecretErrorCode
    message: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        code = self.code.value

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference": reference,
                "code": code,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reference = d.pop("reference")

        code = SecretErrorCode(d.pop("code"))

        message = d.pop("message")

        secret_resolution_error = cls(
            reference=reference,
            code=code,
            message=message,
        )

        secret_resolution_error.additional_properties = d
        return secret_resolution_error

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
