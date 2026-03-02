from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BatchOperationKey,
    lift_batch_operation_key,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_log_actor_type_enum import AuditLogActorTypeEnum
from ..models.batch_operation_state_enum import BatchOperationStateEnum
from ..models.batch_operation_type_enum import BatchOperationTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.batch_operation_error import BatchOperationError


T = TypeVar("T", bound="BatchOperationResponse")


@_attrs_define
class BatchOperationResponse:
    """
    Attributes:
        errors (list[BatchOperationError]): The errors that occurred per partition during the batch operation.
        batch_operation_key (str | Unset): Key or (Operate Legacy ID = UUID) of the batch operation. Example:
            2251799813684321.
        state (BatchOperationStateEnum | Unset): The batch operation state.
        batch_operation_type (BatchOperationTypeEnum | Unset): The type of the batch operation.
        start_date (datetime.datetime | None | Unset): The start date of the batch operation.
            This is `null` if the batch operation has not yet started.
        end_date (datetime.datetime | None | Unset): The end date of the batch operation.
            This is `null` if the batch operation is still running.
        actor_type (AuditLogActorTypeEnum | Unset): The type of actor who performed the operation.
        actor_id (str | Unset): The ID of the actor who performed the operation. Available for batch operations created
            since 8.9.
        operations_total_count (int | Unset): The total number of items contained in this batch operation.
        operations_failed_count (int | Unset): The number of items which failed during execution of the batch operation.
            (e.g. because they are rejected by the Zeebe engine).
        operations_completed_count (int | Unset): The number of successfully completed tasks.
    """

    errors: list[BatchOperationError]
    batch_operation_key: BatchOperationKey | Unset = UNSET
    state: BatchOperationStateEnum | Unset = UNSET
    batch_operation_type: BatchOperationTypeEnum | Unset = UNSET
    start_date: datetime.datetime | None | Unset = UNSET
    end_date: datetime.datetime | None | Unset = UNSET
    actor_type: AuditLogActorTypeEnum | Unset = UNSET
    actor_id: str | Unset = UNSET
    operations_total_count: int | Unset = UNSET
    operations_failed_count: int | Unset = UNSET
    operations_completed_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        errors: list[dict[str, Any]] = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        batch_operation_key = self.batch_operation_key

        state: str | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        batch_operation_type: str | Unset = UNSET
        if not isinstance(self.batch_operation_type, Unset):
            batch_operation_type = self.batch_operation_type.value

        start_date: None | str | Unset
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.datetime):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: None | str | Unset
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        actor_type: str | Unset = UNSET
        if not isinstance(self.actor_type, Unset):
            actor_type = self.actor_type.value

        actor_id = self.actor_id

        operations_total_count = self.operations_total_count

        operations_failed_count = self.operations_failed_count

        operations_completed_count = self.operations_completed_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errors": errors,
            }
        )
        if batch_operation_key is not UNSET:
            field_dict["batchOperationKey"] = batch_operation_key
        if state is not UNSET:
            field_dict["state"] = state
        if batch_operation_type is not UNSET:
            field_dict["batchOperationType"] = batch_operation_type
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if actor_type is not UNSET:
            field_dict["actorType"] = actor_type
        if actor_id is not UNSET:
            field_dict["actorId"] = actor_id
        if operations_total_count is not UNSET:
            field_dict["operationsTotalCount"] = operations_total_count
        if operations_failed_count is not UNSET:
            field_dict["operationsFailedCount"] = operations_failed_count
        if operations_completed_count is not UNSET:
            field_dict["operationsCompletedCount"] = operations_completed_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_operation_error import BatchOperationError

        d = dict(src_dict)
        errors: list[BatchOperationError] = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = BatchOperationError.from_dict(errors_item_data)

            errors.append(errors_item)

        batch_operation_key = (
            lift_batch_operation_key(_val)
            if (_val := d.pop("batchOperationKey", UNSET)) is not UNSET
            else UNSET
        )

        _state = d.pop("state", UNSET)
        state: BatchOperationStateEnum | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = BatchOperationStateEnum(_state)

        _batch_operation_type = d.pop("batchOperationType", UNSET)
        batch_operation_type: BatchOperationTypeEnum | Unset
        if isinstance(_batch_operation_type, Unset):
            batch_operation_type = UNSET
        else:
            batch_operation_type = BatchOperationTypeEnum(_batch_operation_type)

        def _parse_start_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data)

                return start_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_date = _parse_start_date(d.pop("startDate", UNSET))

        def _parse_end_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_date = _parse_end_date(d.pop("endDate", UNSET))

        _actor_type = d.pop("actorType", UNSET)
        actor_type: AuditLogActorTypeEnum | Unset
        if isinstance(_actor_type, Unset):
            actor_type = UNSET
        else:
            actor_type = AuditLogActorTypeEnum(_actor_type)

        actor_id = d.pop("actorId", UNSET)

        operations_total_count = d.pop("operationsTotalCount", UNSET)

        operations_failed_count = d.pop("operationsFailedCount", UNSET)

        operations_completed_count = d.pop("operationsCompletedCount", UNSET)

        batch_operation_response = cls(
            errors=errors,
            batch_operation_key=batch_operation_key,
            state=state,
            batch_operation_type=batch_operation_type,
            start_date=start_date,
            end_date=end_date,
            actor_type=actor_type,
            actor_id=actor_id,
            operations_total_count=operations_total_count,
            operations_failed_count=operations_failed_count,
            operations_completed_count=operations_completed_count,
        )

        batch_operation_response.additional_properties = d
        return batch_operation_response

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
