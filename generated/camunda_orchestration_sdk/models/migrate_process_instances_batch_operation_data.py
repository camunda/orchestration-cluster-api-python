from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.migrate_process_instances_batch_operation_migration_plan import (
        MigrateProcessInstancesBatchOperationMigrationPlan,
    )
    from ..models.process_instance_cancellation_batch_operation_request_filter import (
        ProcessInstanceCancellationBatchOperationRequestFilter,
    )


T = TypeVar("T", bound="MigrateProcessInstancesBatchOperationData")


@_attrs_define
class MigrateProcessInstancesBatchOperationData:
    """
    Attributes:
        filter_ (ProcessInstanceCancellationBatchOperationRequestFilter): The process instance filter.
        migration_plan (MigrateProcessInstancesBatchOperationMigrationPlan): The migration plan.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
    """

    filter_: ProcessInstanceCancellationBatchOperationRequestFilter
    migration_plan: MigrateProcessInstancesBatchOperationMigrationPlan
    operation_reference: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        migration_plan = self.migration_plan.to_dict()

        operation_reference = self.operation_reference

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "filter": filter_,
                "migrationPlan": migration_plan,
            }
        )
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.migrate_process_instances_batch_operation_migration_plan import (
            MigrateProcessInstancesBatchOperationMigrationPlan,
        )
        from ..models.process_instance_cancellation_batch_operation_request_filter import (
            ProcessInstanceCancellationBatchOperationRequestFilter,
        )

        d = dict(src_dict)
        filter_ = ProcessInstanceCancellationBatchOperationRequestFilter.from_dict(
            d.pop("filter")
        )

        migration_plan = MigrateProcessInstancesBatchOperationMigrationPlan.from_dict(
            d.pop("migrationPlan")
        )

        operation_reference = d.pop("operationReference", UNSET)

        migrate_process_instances_batch_operation_data = cls(
            filter_=filter_,
            migration_plan=migration_plan,
            operation_reference=operation_reference,
        )

        return migrate_process_instances_batch_operation_data
