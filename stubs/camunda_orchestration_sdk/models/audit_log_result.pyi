from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import AuditLogEntityKey, AuditLogKey, BatchOperationKey, DecisionDefinitionId, DecisionDefinitionKey, DecisionEvaluationKey, DecisionRequirementsKey, DeploymentKey, ElementInstanceKey, FormKey, JobKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId, UserTaskKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.audit_log_category_enum import AuditLogCategoryEnum
from ..models.audit_log_entity_type_enum import AuditLogEntityTypeEnum
from ..models.audit_log_operation_type_enum import AuditLogOperationTypeEnum
from ..models.audit_log_result_actor_type import AuditLogResultActorType
from ..models.audit_log_result_batch_operation_type import AuditLogResultBatchOperationType
from ..models.audit_log_result_enum import AuditLogResultEnum
from ..models.audit_log_result_related_entity_type import AuditLogResultRelatedEntityType
T = TypeVar("T", bound="AuditLogResult")
@_attrs_define
class AuditLogResult:
    audit_log_key: AuditLogKey
    entity_key: str
    entity_type: AuditLogEntityTypeEnum
    operation_type: AuditLogOperationTypeEnum
    batch_operation_key: None | BatchOperationKey
    batch_operation_type: AuditLogResultBatchOperationType
    timestamp: datetime.datetime
    actor_id: None | str
    actor_type: AuditLogResultActorType
    agent_element_id: None | str
    tenant_id: None | TenantId
    result: AuditLogResultEnum
    annotation: None | str
    category: AuditLogCategoryEnum
    process_definition_id: None | ProcessDefinitionId
    process_definition_key: None | ProcessDefinitionKey
    process_instance_key: None | ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    element_instance_key: None | ElementInstanceKey
    job_key: None | JobKey
    user_task_key: None | UserTaskKey
    decision_requirements_id: None | str
    decision_requirements_key: None | DecisionRequirementsKey
    decision_definition_id: None | DecisionDefinitionId
    decision_definition_key: None | DecisionDefinitionKey
    decision_evaluation_key: None | DecisionEvaluationKey
    deployment_key: None | DeploymentKey
    form_key: None | FormKey
    resource_key: str
    related_entity_key: None | AuditLogEntityKey
    related_entity_type: AuditLogResultRelatedEntityType
    entity_description: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
