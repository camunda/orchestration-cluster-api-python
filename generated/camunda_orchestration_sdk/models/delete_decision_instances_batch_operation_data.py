from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delete_decision_instances_batch_operation_data_filter import (
        DeleteDecisionInstancesBatchOperationDataFilter,
    )


T = TypeVar("T", bound="DeleteDecisionInstancesBatchOperationData")


@_attrs_define
class DeleteDecisionInstancesBatchOperationData:
    """The decision instance filter that defines which decision instances should be deleted.

    Attributes:
        filter_ (DeleteDecisionInstancesBatchOperationDataFilter): The decision instance filter.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
    """

    filter_: DeleteDecisionInstancesBatchOperationDataFilter
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "filter": filter_,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_decision_instances_batch_operation_data_filter import (
            DeleteDecisionInstancesBatchOperationDataFilter,
        )

        d = dict(src_dict)
        filter_ = DeleteDecisionInstancesBatchOperationDataFilter.from_dict(
            d.pop("filter")
        )

        operation_reference = d.pop("operationReference", UNSET)

        delete_decision_instances_batch_operation_data = cls(
            filter_=filter_,
            operation_reference=operation_reference,
        )

        return delete_decision_instances_batch_operation_data
