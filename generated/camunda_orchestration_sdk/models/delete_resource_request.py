from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteResourceRequest")


@_attrs_define
class DeleteResourceRequest:
    """
    Attributes:
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
        delete_history (bool | Unset): Indicates if the historic data associated with the resource should also be
            deleted
            asynchronously.

            This flag is effective for process definitions and decision requirements definitions.
            For other resource types (forms, generic resources) it is ignored and no history is
            deleted. For a decision requirements definition the `batchOperation` field in the
            response carries the created batch operation. For a process definition the history is
            deleted as part of the definition's draining/deletion lifecycle and no batch operation is
            returned.
             Server default: False.
    """

    operation_reference: int | Unset = UNSET
    delete_history: bool | Unset = UNSET

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

        delete_resource_request_type_0 = cls(
            operation_reference=operation_reference,
            delete_history=delete_history,
        )

        return delete_resource_request_type_0
