from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    AuditLogKey,
    BatchOperationKey,
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationKey,
    DecisionRequirementsKey,
    DeploymentKey,
    ElementInstanceKey,
    FormKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    UserTaskKey,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.audit_log_actor_type_enum import AuditLogActorTypeEnum
from ..models.audit_log_category_enum import AuditLogCategoryEnum
from ..models.audit_log_entity_type_enum import AuditLogEntityTypeEnum
from ..models.audit_log_operation_type_enum import AuditLogOperationTypeEnum
from ..models.audit_log_result_batch_operation_type import (
    AuditLogResultBatchOperationType,
)
from ..models.audit_log_result_enum import AuditLogResultEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="AuditLogResult")

@_attrs_define
class AuditLogResult:
    audit_log_key: AuditLogKey | Unset = UNSET
    entity_key: str | Unset = UNSET
    entity_type: AuditLogEntityTypeEnum | Unset = UNSET
    operation_type: AuditLogOperationTypeEnum | Unset = UNSET
    batch_operation_key: BatchOperationKey | Unset = UNSET
    batch_operation_type: AuditLogResultBatchOperationType | Unset = UNSET
    timestamp: datetime.datetime | Unset = UNSET
    actor_id: str | Unset = UNSET
    actor_type: AuditLogActorTypeEnum | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    result: AuditLogResultEnum | Unset = UNSET
    annotation: str | Unset = UNSET
    category: AuditLogCategoryEnum | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    job_key: JobKey | Unset = UNSET
    user_task_key: UserTaskKey | Unset = UNSET
    decision_requirements_id: str | Unset = UNSET
    decision_requirements_key: DecisionRequirementsKey | Unset = UNSET
    decision_definition_id: DecisionDefinitionId | Unset = UNSET
    decision_definition_key: DecisionDefinitionKey | Unset = UNSET
    decision_evaluation_key: DecisionEvaluationKey | Unset = UNSET
    deployment_key: DeploymentKey | Unset = UNSET
    form_key: FormKey | Unset = UNSET
    resource_key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
