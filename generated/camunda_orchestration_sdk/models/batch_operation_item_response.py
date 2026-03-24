from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BatchOperationKey,
    ProcessInstanceKey,
    lift_batch_operation_key,
    lift_process_instance_key,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.batch_operation_item_response_state import BatchOperationItemResponseState
from ..models.batch_operation_type_enum import BatchOperationTypeEnum

T = TypeVar("T", bound="BatchOperationItemResponse")


@_attrs_define
class BatchOperationItemResponse:
    """
    Attributes:
        operation_type (BatchOperationTypeEnum): The type of the batch operation.
        batch_operation_key (str): The key (or operate legacy ID) of the batch operation. Example: 2251799813684321.
        item_key (str): Key of the item, e.g. a process instance key.
        process_instance_key (str): the process instance key of the processed item. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        state (BatchOperationItemResponseState): State of the item.
        processed_date (datetime.datetime | None): The date this item was processed.
            This is `null` if the item has not yet been processed.
        error_message (None | str): The error message from the engine in case of a failed operation.
    """

    operation_type: BatchOperationTypeEnum
    batch_operation_key: BatchOperationKey
    item_key: str
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    state: BatchOperationItemResponseState
    processed_date: datetime.datetime | None
    error_message: None | str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        operation_type = self.operation_type.value

        batch_operation_key = self.batch_operation_key

        item_key = self.item_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        state = self.state.value

        processed_date: None | str
        if isinstance(self.processed_date, datetime.datetime):
            processed_date = self.processed_date.isoformat()
        else:
            processed_date = self.processed_date

        error_message: None | str
        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operationType": operation_type,
                "batchOperationKey": batch_operation_key,
                "itemKey": item_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "state": state,
                "processedDate": processed_date,
                "errorMessage": error_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation_type = BatchOperationTypeEnum(d.pop("operationType"))

        batch_operation_key = lift_batch_operation_key(d.pop("batchOperationKey"))

        item_key = d.pop("itemKey")

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = lift_process_instance_key(
            _raw_root_process_instance_key
        )

        state = BatchOperationItemResponseState(d.pop("state"))

        def _parse_processed_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                processed_date_type_0 = isoparse(data)

                return processed_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        processed_date = _parse_processed_date(d.pop("processedDate"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("errorMessage"))

        batch_operation_item_response = cls(
            operation_type=operation_type,
            batch_operation_key=batch_operation_key,
            item_key=item_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            state=state,
            processed_date=processed_date,
            error_message=error_message,
        )

        batch_operation_item_response.additional_properties = d
        return batch_operation_item_response

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
