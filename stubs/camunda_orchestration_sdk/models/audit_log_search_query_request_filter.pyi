from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.audit_log_actor_type_exact_match import AuditLogActorTypeExactMatch
from ..models.audit_log_result_exact_match import AuditLogResultExactMatch
from ..models.batch_operation_type_exact_match import BatchOperationTypeExactMatch
from ..models.category_exact_match import CategoryExactMatch
from ..models.entity_type_exact_match import EntityTypeExactMatch
from ..models.operation_type_exact_match import OperationTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
from ..models.advanced_audit_log_entity_key_filter import AdvancedAuditLogEntityKeyFilter
from ..models.advanced_audit_log_key_filter import AdvancedAuditLogKeyFilter
from ..models.advanced_batch_operation_type_filter import AdvancedBatchOperationTypeFilter
from ..models.advanced_category_filter import AdvancedCategoryFilter
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_decision_definition_key_filter import AdvancedDecisionDefinitionKeyFilter
from ..models.advanced_decision_evaluation_key_filter import AdvancedDecisionEvaluationKeyFilter
from ..models.advanced_decision_requirements_key_filter import AdvancedDecisionRequirementsKeyFilter
from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
from ..models.advanced_element_instance_key_filter import AdvancedElementInstanceKeyFilter
from ..models.advanced_entity_type_filter import AdvancedEntityTypeFilter
from ..models.advanced_form_key_filter import AdvancedFormKeyFilter
from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
from ..models.advanced_process_definition_key_filter import AdvancedProcessDefinitionKeyFilter
from ..models.advanced_process_instance_key_filter import AdvancedProcessInstanceKeyFilter
from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
from ..models.advanced_result_filter import AdvancedResultFilter
from ..models.advanced_string_filter import AdvancedStringFilter
from ..models.basic_string_filter import BasicStringFilter
T = TypeVar("T", bound="AuditLogSearchQueryRequestFilter")
@_attrs_define
class AuditLogSearchQueryRequestFilter:
    audit_log_key: AdvancedAuditLogKeyFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    operation_type: AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset = (
            UNSET
        )
    result: AdvancedResultFilter | AuditLogResultExactMatch | Unset = UNSET
    timestamp: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    actor_id: AdvancedStringFilter | str | Unset = UNSET
    actor_type: AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset = UNSET
    entity_key: AdvancedAuditLogEntityKeyFilter | str | Unset = UNSET
    entity_type: AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    category: AdvancedCategoryFilter | CategoryExactMatch | Unset = UNSET
    deployment_key: AdvancedDeploymentKeyFilter | str | Unset = UNSET
    form_key: AdvancedFormKeyFilter | str | Unset = UNSET
    resource_key: AdvancedResourceKeyFilter | str | Unset = UNSET
    batch_operation_type: (
            AdvancedBatchOperationTypeFilter | BatchOperationTypeExactMatch | Unset
        ) = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    job_key: AdvancedJobKeyFilter | str | Unset = UNSET
    user_task_key: BasicStringFilter | str | Unset = UNSET
    decision_requirements_id: AdvancedStringFilter | str | Unset = UNSET
    decision_requirements_key: AdvancedDecisionRequirementsKeyFilter | str | Unset = (
            UNSET
        )
    decision_definition_id: AdvancedStringFilter | str | Unset = UNSET
    decision_definition_key: AdvancedDecisionDefinitionKeyFilter | str | Unset = UNSET
    decision_evaluation_key: AdvancedDecisionEvaluationKeyFilter | str | Unset = UNSET
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
