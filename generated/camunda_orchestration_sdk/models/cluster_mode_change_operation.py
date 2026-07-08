from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClusterModeChangeOperation")


@_attrs_define
class ClusterModeChangeOperation:
    """A single operation that is part of a cluster mode change.

    Attributes:
        operation (str): The type of the operation. Example: ModeChangeOperation.
        mode (None | str): The target mode of the operation, if applicable. Example: RECOVERING.
    """

    operation: str
    mode: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        operation = self.operation

        mode: None | str
        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation": operation,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation = d.pop("operation")

        def _parse_mode(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mode = _parse_mode(d.pop("mode"))

        cluster_mode_change_operation = cls(
            operation=operation,
            mode=mode,
        )

        cluster_mode_change_operation.additional_properties = d
        return cluster_mode_change_operation

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
