from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteResourceDataType0")


@_attrs_define
class DeleteResourceDataType0:
    """
    Attributes:
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
        delete_history (bool | Unset): Indicates if the historic data of a process resource should be deleted via a
            batch operation asynchronously.

            This flag is only effective for process resources. For other resource types
            (decisions, forms, generic resources), this flag is ignored and no history
            will be deleted. In those cases, the `batchOperation` field in the response
            will not be populated.
             Default: False.
    """

    operation_reference: int | Unset = UNSET
    delete_history: bool | Unset = False

    def to_dict(self) -> dict[str, Any]:
        operation_reference = self.operation_reference

        delete_history = self.delete_history

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference
        if delete_history is not UNSET:
            field_dict["deleteHistory"] = delete_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation_reference = d.pop("operationReference", UNSET)

        delete_history = d.pop("deleteHistory", UNSET)

        delete_resource_data_type_0 = cls(
            operation_reference=operation_reference,
            delete_history=delete_history,
        )

        return delete_resource_data_type_0
