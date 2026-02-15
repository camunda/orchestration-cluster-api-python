from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.migrate_process_instances_batch_operation_migration_plan import MigrateProcessInstancesBatchOperationMigrationPlan
from ..models.process_instance_cancellation_batch_operation_request_filter import ProcessInstanceCancellationBatchOperationRequestFilter
T = TypeVar("T", bound="MigrateProcessInstancesBatchOperationData")
@_attrs_define
class MigrateProcessInstancesBatchOperationData:
    filter_: ProcessInstanceCancellationBatchOperationRequestFilter
    migration_plan: MigrateProcessInstancesBatchOperationMigrationPlan
    operation_reference: int | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
