from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BatchOperationKey,
    lift_batch_operation_key,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.batch_operation_type_enum import BatchOperationTypeEnum

T = TypeVar("T", bound="DeleteResourceResponseBatchOperation")


@_attrs_define
class DeleteResourceResponseBatchOperation:
    """The batch operation created for asynchronously deleting the historic data.

    This field is only populated when the request `deleteHistory` is set to `true` and the resource
    is a process definition. For other resource types (decisions, forms, generic resources),
    this field will be `null`.

        Attributes:
            batch_operation_key (str): Key of the batch operation. Example: 2251799813684321.
            batch_operation_type (BatchOperationTypeEnum): The type of the batch operation.
    """

    batch_operation_key: BatchOperationKey
    batch_operation_type: BatchOperationTypeEnum
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        batch_operation_key = self.batch_operation_key

        batch_operation_type = self.batch_operation_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batchOperationKey": batch_operation_key,
                "batchOperationType": batch_operation_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batch_operation_key = lift_batch_operation_key(d.pop("batchOperationKey"))

        batch_operation_type = BatchOperationTypeEnum(d.pop("batchOperationType"))

        delete_resource_response_batch_operation = cls(
            batch_operation_key=batch_operation_key,
            batch_operation_type=batch_operation_type,
        )

        delete_resource_response_batch_operation.additional_properties = d
        return delete_resource_response_batch_operation

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
