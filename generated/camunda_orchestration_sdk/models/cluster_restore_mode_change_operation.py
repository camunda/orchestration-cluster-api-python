from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClusterRestoreModeChangeOperation")


@_attrs_define
class ClusterRestoreModeChangeOperation:
    """The operation that transitions a broker to a mode once its partitions are restored.

    Attributes:
        operation (str): The type of the operation. Example: ModeChangeOperation.
        broker_id (str): The ID of the broker that applies the operation, including its zone if it belongs to one.
            Example: 1.
        mode (str): The mode the broker is transitioned to. Example: PROCESSING.
    """

    operation: str
    broker_id: str
    mode: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        operation = self.operation

        broker_id = self.broker_id

        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation": operation,
                "brokerId": broker_id,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation = d.pop("operation")

        broker_id = d.pop("brokerId")

        mode = d.pop("mode")

        cluster_restore_mode_change_operation = cls(
            operation=operation,
            broker_id=broker_id,
            mode=mode,
        )

        cluster_restore_mode_change_operation.additional_properties = d
        return cluster_restore_mode_change_operation

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
