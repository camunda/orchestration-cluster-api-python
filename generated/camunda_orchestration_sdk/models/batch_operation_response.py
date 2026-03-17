from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BatchOperationKey,
    lift_batch_operation_key,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.batch_operation_response_actor_type import BatchOperationResponseActorType
from ..models.batch_operation_state_enum import BatchOperationStateEnum
from ..models.batch_operation_type_enum import BatchOperationTypeEnum

if TYPE_CHECKING:
    from ..models.batch_operation_error import BatchOperationError


T = TypeVar("T", bound="BatchOperationResponse")


@_attrs_define
class BatchOperationResponse:
    """
    Attributes:
        batch_operation_key (str): Key or (Operate Legacy ID = UUID) of the batch operation. Example: 2251799813684321.
        state (BatchOperationStateEnum): The batch operation state.
        batch_operation_type (BatchOperationTypeEnum): The type of the batch operation.
        start_date (datetime.datetime | None): The start date of the batch operation.
            This is `null` if the batch operation has not yet started.
        end_date (datetime.datetime | None): The end date of the batch operation.
            This is `null` if the batch operation is still running.
        actor_type (BatchOperationResponseActorType): The type of the actor who performed the operation.
            This is `null` if the batch operation was created before 8.9,
            or if the actor information is not available.
        actor_id (None | str): The ID of the actor who performed the operation. Available for batch operations created
            since 8.9.
        operations_total_count (int): The total number of items contained in this batch operation.
        operations_failed_count (int): The number of items which failed during execution of the batch operation. (e.g.
            because they are rejected by the Zeebe engine).
        operations_completed_count (int): The number of successfully completed tasks.
        errors (list[BatchOperationError]): The errors that occurred per partition during the batch operation.
    """

    batch_operation_key: BatchOperationKey
    state: BatchOperationStateEnum
    batch_operation_type: BatchOperationTypeEnum
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None
    actor_type: BatchOperationResponseActorType
    actor_id: None | str
    operations_total_count: int
    operations_failed_count: int
    operations_completed_count: int
    errors: list[BatchOperationError]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        batch_operation_key = self.batch_operation_key

        state = self.state.value

        batch_operation_type = self.batch_operation_type.value

        start_date: None | str
        if isinstance(self.start_date, datetime.datetime):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: None | str
        if isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        actor_type = self.actor_type.value

        actor_id: None | str
        actor_id = self.actor_id

        operations_total_count = self.operations_total_count

        operations_failed_count = self.operations_failed_count

        operations_completed_count = self.operations_completed_count

        errors: list[dict[str, Any]] = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batchOperationKey": batch_operation_key,
                "state": state,
                "batchOperationType": batch_operation_type,
                "startDate": start_date,
                "endDate": end_date,
                "actorType": actor_type,
                "actorId": actor_id,
                "operationsTotalCount": operations_total_count,
                "operationsFailedCount": operations_failed_count,
                "operationsCompletedCount": operations_completed_count,
                "errors": errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_operation_error import BatchOperationError

        d = dict(src_dict)
        batch_operation_key = lift_batch_operation_key(d.pop("batchOperationKey"))

        state = BatchOperationStateEnum(d.pop("state"))

        batch_operation_type = BatchOperationTypeEnum(d.pop("batchOperationType"))

        def _parse_start_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data)

                return start_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        start_date = _parse_start_date(d.pop("startDate"))

        def _parse_end_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        end_date = _parse_end_date(d.pop("endDate"))

        actor_type = BatchOperationResponseActorType(d.pop("actorType"))

        def _parse_actor_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_id = _parse_actor_id(d.pop("actorId"))

        operations_total_count = d.pop("operationsTotalCount")

        operations_failed_count = d.pop("operationsFailedCount")

        operations_completed_count = d.pop("operationsCompletedCount")

        errors: list[BatchOperationError] = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = BatchOperationError.from_dict(errors_item_data)

            errors.append(errors_item)

        batch_operation_response = cls(
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
            errors=errors,
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
