from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.batch_operation_error_type import BatchOperationErrorType

T = TypeVar("T", bound="BatchOperationError")


@_attrs_define
class BatchOperationError:
    """
    Attributes:
        partition_id (int): The partition ID where the error occurred.
        type_ (BatchOperationErrorType): The type of the error that occurred during the batch operation.
        message (str): The error message that occurred during the batch operation.
    """

    partition_id: int
    type_: BatchOperationErrorType
    message: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        partition_id = self.partition_id

        type_ = self.type_.value

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "type": type_,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        type_ = BatchOperationErrorType(d.pop("type"))

        message = d.pop("message")

        batch_operation_error = cls(
            partition_id=partition_id,
            type_=type_,
            message=message,
        )

        batch_operation_error.additional_properties = d
        return batch_operation_error

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
