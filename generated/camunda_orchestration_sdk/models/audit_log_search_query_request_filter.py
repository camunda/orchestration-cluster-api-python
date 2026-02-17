from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_log_actor_type_exact_match import AuditLogActorTypeExactMatch
from ..models.audit_log_result_exact_match import AuditLogResultExactMatch
from ..models.batch_operation_type_exact_match import BatchOperationTypeExactMatch
from ..models.category_exact_match import CategoryExactMatch
from ..models.entity_type_exact_match import EntityTypeExactMatch
from ..models.operation_type_exact_match import OperationTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
    from ..models.advanced_audit_log_entity_key_filter import (
        AdvancedAuditLogEntityKeyFilter,
    )
    from ..models.advanced_audit_log_key_filter import AdvancedAuditLogKeyFilter
    from ..models.advanced_batch_operation_type_filter import (
        AdvancedBatchOperationTypeFilter,
    )
    from ..models.advanced_category_filter import AdvancedCategoryFilter
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_decision_definition_key_filter import (
        AdvancedDecisionDefinitionKeyFilter,
    )
    from ..models.advanced_decision_evaluation_key_filter import (
        AdvancedDecisionEvaluationKeyFilter,
    )
    from ..models.advanced_decision_requirements_key_filter import (
        AdvancedDecisionRequirementsKeyFilter,
    )
    from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_entity_type_filter import AdvancedEntityTypeFilter
    from ..models.advanced_form_key_filter import AdvancedFormKeyFilter
    from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
    from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
    from ..models.advanced_result_filter import AdvancedResultFilter
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.basic_string_filter import BasicStringFilter


T = TypeVar("T", bound="AuditLogSearchQueryRequestFilter")


@_attrs_define
class AuditLogSearchQueryRequestFilter:
    """The audit log search filters.

    Attributes:
        audit_log_key (AdvancedAuditLogKeyFilter | str | Unset):
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset):
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset):
        operation_type (AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset):
        result (AdvancedResultFilter | AuditLogResultExactMatch | Unset):
        timestamp (AdvancedDateTimeFilter | datetime.datetime | Unset):
        actor_id (AdvancedStringFilter | str | Unset):
        actor_type (AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset):
        agent_element_id (AdvancedStringFilter | str | Unset):
        entity_key (AdvancedAuditLogEntityKeyFilter | str | Unset):
        entity_type (AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
        category (AdvancedCategoryFilter | CategoryExactMatch | Unset):
        deployment_key (AdvancedDeploymentKeyFilter | str | Unset):
        form_key (AdvancedFormKeyFilter | str | Unset):
        resource_key (AdvancedResourceKeyFilter | str | Unset):
        batch_operation_type (AdvancedBatchOperationTypeFilter | BatchOperationTypeExactMatch | Unset):
        process_definition_id (AdvancedStringFilter | str | Unset):
        job_key (AdvancedJobKeyFilter | str | Unset):
        user_task_key (BasicStringFilter | str | Unset):
        decision_requirements_id (AdvancedStringFilter | str | Unset):
        decision_requirements_key (AdvancedDecisionRequirementsKeyFilter | str | Unset):
        decision_definition_id (AdvancedStringFilter | str | Unset):
        decision_definition_key (AdvancedDecisionDefinitionKeyFilter | str | Unset):
        decision_evaluation_key (AdvancedDecisionEvaluationKeyFilter | str | Unset):
        related_entity_key (AdvancedAuditLogEntityKeyFilter | str | Unset):
        related_entity_type (AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset):
        entity_description (AdvancedStringFilter | str | Unset):
    """

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
    agent_element_id: AdvancedStringFilter | str | Unset = UNSET
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
    related_entity_key: AdvancedAuditLogEntityKeyFilter | str | Unset = UNSET
    related_entity_type: AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset = UNSET
    entity_description: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_audit_log_entity_key_filter import (
            AdvancedAuditLogEntityKeyFilter,
        )
        from ..models.advanced_audit_log_key_filter import AdvancedAuditLogKeyFilter
        from ..models.advanced_decision_definition_key_filter import (
            AdvancedDecisionDefinitionKeyFilter,
        )
        from ..models.advanced_decision_evaluation_key_filter import (
            AdvancedDecisionEvaluationKeyFilter,
        )
        from ..models.advanced_decision_requirements_key_filter import (
            AdvancedDecisionRequirementsKeyFilter,
        )
        from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_form_key_filter import AdvancedFormKeyFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.basic_string_filter import BasicStringFilter

        audit_log_key: dict[str, Any] | str | Unset
        if isinstance(self.audit_log_key, Unset):
            audit_log_key = UNSET
        elif isinstance(self.audit_log_key, AdvancedAuditLogKeyFilter):
            audit_log_key = self.audit_log_key.to_dict()
        else:
            audit_log_key = self.audit_log_key

        process_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_key, Unset):
            process_definition_key = UNSET
        elif isinstance(
            self.process_definition_key, AdvancedProcessDefinitionKeyFilter
        ):
            process_definition_key = self.process_definition_key.to_dict()
        else:
            process_definition_key = self.process_definition_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, AdvancedElementInstanceKeyFilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        operation_type: dict[str, Any] | str | Unset
        if isinstance(self.operation_type, Unset):
            operation_type = UNSET
        elif isinstance(self.operation_type, OperationTypeExactMatch):
            operation_type = self.operation_type.value
        else:
            operation_type = self.operation_type.to_dict()

        result: dict[str, Any] | str | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, AuditLogResultExactMatch):
            result = self.result.value
        else:
            result = self.result.to_dict()

        timestamp: dict[str, Any] | str | Unset
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        elif isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp.to_dict()

        actor_id: dict[str, Any] | str | Unset
        if isinstance(self.actor_id, Unset):
            actor_id = UNSET
        elif isinstance(self.actor_id, AdvancedStringFilter):
            actor_id = self.actor_id.to_dict()
        else:
            actor_id = self.actor_id

        actor_type: dict[str, Any] | str | Unset
        if isinstance(self.actor_type, Unset):
            actor_type = UNSET
        elif isinstance(self.actor_type, AuditLogActorTypeExactMatch):
            actor_type = self.actor_type.value
        else:
            actor_type = self.actor_type.to_dict()

        agent_element_id: dict[str, Any] | str | Unset
        if isinstance(self.agent_element_id, Unset):
            agent_element_id = UNSET
        elif isinstance(self.agent_element_id, AdvancedStringFilter):
            agent_element_id = self.agent_element_id.to_dict()
        else:
            agent_element_id = self.agent_element_id

        entity_key: dict[str, Any] | str | Unset
        if isinstance(self.entity_key, Unset):
            entity_key = UNSET
        elif isinstance(self.entity_key, AdvancedAuditLogEntityKeyFilter):
            entity_key = self.entity_key.to_dict()
        else:
            entity_key = self.entity_key

        entity_type: dict[str, Any] | str | Unset
        if isinstance(self.entity_type, Unset):
            entity_type = UNSET
        elif isinstance(self.entity_type, EntityTypeExactMatch):
            entity_type = self.entity_type.value
        else:
            entity_type = self.entity_type.to_dict()

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        category: dict[str, Any] | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, CategoryExactMatch):
            category = self.category.value
        else:
            category = self.category.to_dict()

        deployment_key: dict[str, Any] | str | Unset
        if isinstance(self.deployment_key, Unset):
            deployment_key = UNSET
        elif isinstance(self.deployment_key, AdvancedDeploymentKeyFilter):
            deployment_key = self.deployment_key.to_dict()
        else:
            deployment_key = self.deployment_key

        form_key: dict[str, Any] | str | Unset
        if isinstance(self.form_key, Unset):
            form_key = UNSET
        elif isinstance(self.form_key, AdvancedFormKeyFilter):
            form_key = self.form_key.to_dict()
        else:
            form_key = self.form_key

        resource_key: dict[str, Any] | str | Unset
        if isinstance(self.resource_key, Unset):
            resource_key = UNSET
        elif isinstance(self.resource_key, AdvancedResourceKeyFilter):
            resource_key = self.resource_key.to_dict()
        else:
            resource_key = self.resource_key

        batch_operation_type: dict[str, Any] | str | Unset
        if isinstance(self.batch_operation_type, Unset):
            batch_operation_type = UNSET
        elif isinstance(self.batch_operation_type, BatchOperationTypeExactMatch):
            batch_operation_type = self.batch_operation_type.value
        else:
            batch_operation_type = self.batch_operation_type.to_dict()

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, AdvancedStringFilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        job_key: dict[str, Any] | str | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        elif isinstance(self.job_key, AdvancedJobKeyFilter):
            job_key = self.job_key.to_dict()
        else:
            job_key = self.job_key

        user_task_key: dict[str, Any] | str | Unset
        if isinstance(self.user_task_key, Unset):
            user_task_key = UNSET
        elif isinstance(self.user_task_key, BasicStringFilter):
            user_task_key = self.user_task_key.to_dict()
        else:
            user_task_key = self.user_task_key

        decision_requirements_id: dict[str, Any] | str | Unset
        if isinstance(self.decision_requirements_id, Unset):
            decision_requirements_id = UNSET
        elif isinstance(self.decision_requirements_id, AdvancedStringFilter):
            decision_requirements_id = self.decision_requirements_id.to_dict()
        else:
            decision_requirements_id = self.decision_requirements_id

        decision_requirements_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_requirements_key, Unset):
            decision_requirements_key = UNSET
        elif isinstance(
            self.decision_requirements_key, AdvancedDecisionRequirementsKeyFilter
        ):
            decision_requirements_key = self.decision_requirements_key.to_dict()
        else:
            decision_requirements_key = self.decision_requirements_key

        decision_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.decision_definition_id, Unset):
            decision_definition_id = UNSET
        elif isinstance(self.decision_definition_id, AdvancedStringFilter):
            decision_definition_id = self.decision_definition_id.to_dict()
        else:
            decision_definition_id = self.decision_definition_id

        decision_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_definition_key, Unset):
            decision_definition_key = UNSET
        elif isinstance(
            self.decision_definition_key, AdvancedDecisionDefinitionKeyFilter
        ):
            decision_definition_key = self.decision_definition_key.to_dict()
        else:
            decision_definition_key = self.decision_definition_key

        decision_evaluation_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_evaluation_key, Unset):
            decision_evaluation_key = UNSET
        elif isinstance(
            self.decision_evaluation_key, AdvancedDecisionEvaluationKeyFilter
        ):
            decision_evaluation_key = self.decision_evaluation_key.to_dict()
        else:
            decision_evaluation_key = self.decision_evaluation_key

        related_entity_key: dict[str, Any] | str | Unset
        if isinstance(self.related_entity_key, Unset):
            related_entity_key = UNSET
        elif isinstance(self.related_entity_key, AdvancedAuditLogEntityKeyFilter):
            related_entity_key = self.related_entity_key.to_dict()
        else:
            related_entity_key = self.related_entity_key

        related_entity_type: dict[str, Any] | str | Unset
        if isinstance(self.related_entity_type, Unset):
            related_entity_type = UNSET
        elif isinstance(self.related_entity_type, EntityTypeExactMatch):
            related_entity_type = self.related_entity_type.value
        else:
            related_entity_type = self.related_entity_type.to_dict()

        entity_description: dict[str, Any] | str | Unset
        if isinstance(self.entity_description, Unset):
            entity_description = UNSET
        elif isinstance(self.entity_description, AdvancedStringFilter):
            entity_description = self.entity_description.to_dict()
        else:
            entity_description = self.entity_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if audit_log_key is not UNSET:
            field_dict["auditLogKey"] = audit_log_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if operation_type is not UNSET:
            field_dict["operationType"] = operation_type
        if result is not UNSET:
            field_dict["result"] = result
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if actor_id is not UNSET:
            field_dict["actorId"] = actor_id
        if actor_type is not UNSET:
            field_dict["actorType"] = actor_type
        if agent_element_id is not UNSET:
            field_dict["agentElementId"] = agent_element_id
        if entity_key is not UNSET:
            field_dict["entityKey"] = entity_key
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if category is not UNSET:
            field_dict["category"] = category
        if deployment_key is not UNSET:
            field_dict["deploymentKey"] = deployment_key
        if form_key is not UNSET:
            field_dict["formKey"] = form_key
        if resource_key is not UNSET:
            field_dict["resourceKey"] = resource_key
        if batch_operation_type is not UNSET:
            field_dict["batchOperationType"] = batch_operation_type
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if job_key is not UNSET:
            field_dict["jobKey"] = job_key
        if user_task_key is not UNSET:
            field_dict["userTaskKey"] = user_task_key
        if decision_requirements_id is not UNSET:
            field_dict["decisionRequirementsId"] = decision_requirements_id
        if decision_requirements_key is not UNSET:
            field_dict["decisionRequirementsKey"] = decision_requirements_key
        if decision_definition_id is not UNSET:
            field_dict["decisionDefinitionId"] = decision_definition_id
        if decision_definition_key is not UNSET:
            field_dict["decisionDefinitionKey"] = decision_definition_key
        if decision_evaluation_key is not UNSET:
            field_dict["decisionEvaluationKey"] = decision_evaluation_key
        if related_entity_key is not UNSET:
            field_dict["relatedEntityKey"] = related_entity_key
        if related_entity_type is not UNSET:
            field_dict["relatedEntityType"] = related_entity_type
        if entity_description is not UNSET:
            field_dict["entityDescription"] = entity_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
        from ..models.advanced_audit_log_entity_key_filter import (
            AdvancedAuditLogEntityKeyFilter,
        )
        from ..models.advanced_audit_log_key_filter import AdvancedAuditLogKeyFilter
        from ..models.advanced_batch_operation_type_filter import (
            AdvancedBatchOperationTypeFilter,
        )
        from ..models.advanced_category_filter import AdvancedCategoryFilter
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_decision_definition_key_filter import (
            AdvancedDecisionDefinitionKeyFilter,
        )
        from ..models.advanced_decision_evaluation_key_filter import (
            AdvancedDecisionEvaluationKeyFilter,
        )
        from ..models.advanced_decision_requirements_key_filter import (
            AdvancedDecisionRequirementsKeyFilter,
        )
        from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_entity_type_filter import AdvancedEntityTypeFilter
        from ..models.advanced_form_key_filter import AdvancedFormKeyFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
        from ..models.advanced_result_filter import AdvancedResultFilter
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.basic_string_filter import BasicStringFilter

        d = dict(src_dict)

        def _parse_audit_log_key(
            data: object,
        ) -> AdvancedAuditLogKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                audit_log_key_type_1 = AdvancedAuditLogKeyFilter.from_dict(data)

                return audit_log_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAuditLogKeyFilter | str | Unset, data)

        audit_log_key = _parse_audit_log_key(d.pop("auditLogKey", UNSET))

        def _parse_process_definition_key(
            data: object,
        ) -> AdvancedProcessDefinitionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_key_type_1 = (
                    AdvancedProcessDefinitionKeyFilter.from_dict(data)
                )

                return process_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessDefinitionKeyFilter | str | Unset, data)

        process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey", UNSET)
        )

        def _parse_process_instance_key(
            data: object,
        ) -> AdvancedProcessInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_instance_key_type_1 = (
                    AdvancedProcessInstanceKeyFilter.from_dict(data)
                )

                return process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessInstanceKeyFilter | str | Unset, data)

        process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey", UNSET)
        )

        def _parse_element_instance_key(
            data: object,
        ) -> AdvancedElementInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_instance_key_type_1 = (
                    AdvancedElementInstanceKeyFilter.from_dict(data)
                )

                return element_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementInstanceKeyFilter | str | Unset, data)

        element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey", UNSET)
        )

        def _parse_operation_type(
            data: object,
        ) -> AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_type_type_0 = OperationTypeExactMatch(data)

                return operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            operation_type_type_1 = AdvancedOperationTypeFilter.from_dict(data)

            return operation_type_type_1

        operation_type = _parse_operation_type(d.pop("operationType", UNSET))

        def _parse_result(
            data: object,
        ) -> AdvancedResultFilter | AuditLogResultExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_type_0 = AuditLogResultExactMatch(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            result_type_1 = AdvancedResultFilter.from_dict(data)

            return result_type_1

        result = _parse_result(d.pop("result", UNSET))

        def _parse_timestamp(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = isoparse(data)

                return timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            timestamp_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return timestamp_type_1

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_actor_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                actor_id_type_1 = AdvancedStringFilter.from_dict(data)

                return actor_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        actor_id = _parse_actor_id(d.pop("actorId", UNSET))

        def _parse_actor_type(
            data: object,
        ) -> AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actor_type_type_0 = AuditLogActorTypeExactMatch(data)

                return actor_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            actor_type_type_1 = AdvancedActorTypeFilter.from_dict(data)

            return actor_type_type_1

        actor_type = _parse_actor_type(d.pop("actorType", UNSET))

        def _parse_agent_element_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                agent_element_id_type_1 = AdvancedStringFilter.from_dict(data)

                return agent_element_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        agent_element_id = _parse_agent_element_id(d.pop("agentElementId", UNSET))

        def _parse_entity_key(
            data: object,
        ) -> AdvancedAuditLogEntityKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                entity_key_type_1 = AdvancedAuditLogEntityKeyFilter.from_dict(data)

                return entity_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAuditLogEntityKeyFilter | str | Unset, data)

        entity_key = _parse_entity_key(d.pop("entityKey", UNSET))

        def _parse_entity_type(
            data: object,
        ) -> AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_type_type_0 = EntityTypeExactMatch(data)

                return entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            entity_type_type_1 = AdvancedEntityTypeFilter.from_dict(data)

            return entity_type_type_1

        entity_type = _parse_entity_type(d.pop("entityType", UNSET))

        def _parse_tenant_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                tenant_id_type_1 = AdvancedStringFilter.from_dict(data)

                return tenant_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenantId", UNSET))

        def _parse_category(
            data: object,
        ) -> AdvancedCategoryFilter | CategoryExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_0 = CategoryExactMatch(data)

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            category_type_1 = AdvancedCategoryFilter.from_dict(data)

            return category_type_1

        category = _parse_category(d.pop("category", UNSET))

        def _parse_deployment_key(
            data: object,
        ) -> AdvancedDeploymentKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                deployment_key_type_1 = AdvancedDeploymentKeyFilter.from_dict(data)

                return deployment_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDeploymentKeyFilter | str | Unset, data)

        deployment_key = _parse_deployment_key(d.pop("deploymentKey", UNSET))

        def _parse_form_key(data: object) -> AdvancedFormKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                form_key_type_1 = AdvancedFormKeyFilter.from_dict(data)

                return form_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedFormKeyFilter | str | Unset, data)

        form_key = _parse_form_key(d.pop("formKey", UNSET))

        def _parse_resource_key(
            data: object,
        ) -> AdvancedResourceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                resource_key_type_1 = AdvancedResourceKeyFilter.from_dict(data)

                return resource_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedResourceKeyFilter | str | Unset, data)

        resource_key = _parse_resource_key(d.pop("resourceKey", UNSET))

        def _parse_batch_operation_type(
            data: object,
        ) -> AdvancedBatchOperationTypeFilter | BatchOperationTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                batch_operation_type_type_0 = BatchOperationTypeExactMatch(data)

                return batch_operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            batch_operation_type_type_1 = AdvancedBatchOperationTypeFilter.from_dict(
                data
            )

            return batch_operation_type_type_1

        batch_operation_type = _parse_batch_operation_type(
            d.pop("batchOperationType", UNSET)
        )

        def _parse_process_definition_id(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_id_type_1 = AdvancedStringFilter.from_dict(data)

                return process_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId", UNSET)
        )

        def _parse_job_key(data: object) -> AdvancedJobKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                job_key_type_1 = AdvancedJobKeyFilter.from_dict(data)

                return job_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedJobKeyFilter | str | Unset, data)

        job_key = _parse_job_key(d.pop("jobKey", UNSET))

        def _parse_user_task_key(data: object) -> BasicStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                user_task_key_type_1 = BasicStringFilter.from_dict(data)

                return user_task_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BasicStringFilter | str | Unset, data)

        user_task_key = _parse_user_task_key(d.pop("userTaskKey", UNSET))

        def _parse_decision_requirements_id(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_requirements_id_type_1 = AdvancedStringFilter.from_dict(data)

                return decision_requirements_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        decision_requirements_id = _parse_decision_requirements_id(
            d.pop("decisionRequirementsId", UNSET)
        )

        def _parse_decision_requirements_key(
            data: object,
        ) -> AdvancedDecisionRequirementsKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_requirements_key_type_1 = (
                    AdvancedDecisionRequirementsKeyFilter.from_dict(data)
                )

                return decision_requirements_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDecisionRequirementsKeyFilter | str | Unset, data)

        decision_requirements_key = _parse_decision_requirements_key(
            d.pop("decisionRequirementsKey", UNSET)
        )

        def _parse_decision_definition_id(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_definition_id_type_1 = AdvancedStringFilter.from_dict(data)

                return decision_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        decision_definition_id = _parse_decision_definition_id(
            d.pop("decisionDefinitionId", UNSET)
        )

        def _parse_decision_definition_key(
            data: object,
        ) -> AdvancedDecisionDefinitionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_definition_key_type_1 = (
                    AdvancedDecisionDefinitionKeyFilter.from_dict(data)
                )

                return decision_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDecisionDefinitionKeyFilter | str | Unset, data)

        decision_definition_key = _parse_decision_definition_key(
            d.pop("decisionDefinitionKey", UNSET)
        )

        def _parse_decision_evaluation_key(
            data: object,
        ) -> AdvancedDecisionEvaluationKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_evaluation_key_type_1 = (
                    AdvancedDecisionEvaluationKeyFilter.from_dict(data)
                )

                return decision_evaluation_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDecisionEvaluationKeyFilter | str | Unset, data)

        decision_evaluation_key = _parse_decision_evaluation_key(
            d.pop("decisionEvaluationKey", UNSET)
        )

        def _parse_related_entity_key(
            data: object,
        ) -> AdvancedAuditLogEntityKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                related_entity_key_type_1 = AdvancedAuditLogEntityKeyFilter.from_dict(
                    data
                )

                return related_entity_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAuditLogEntityKeyFilter | str | Unset, data)

        related_entity_key = _parse_related_entity_key(d.pop("relatedEntityKey", UNSET))

        def _parse_related_entity_type(
            data: object,
        ) -> AdvancedEntityTypeFilter | EntityTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                related_entity_type_type_0 = EntityTypeExactMatch(data)

                return related_entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            related_entity_type_type_1 = AdvancedEntityTypeFilter.from_dict(data)

            return related_entity_type_type_1

        related_entity_type = _parse_related_entity_type(
            d.pop("relatedEntityType", UNSET)
        )

        def _parse_entity_description(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                entity_description_type_1 = AdvancedStringFilter.from_dict(data)

                return entity_description_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        entity_description = _parse_entity_description(
            d.pop("entityDescription", UNSET)
        )

        audit_log_search_query_request_filter = cls(
            audit_log_key=audit_log_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            operation_type=operation_type,
            result=result,
            timestamp=timestamp,
            actor_id=actor_id,
            actor_type=actor_type,
            agent_element_id=agent_element_id,
            entity_key=entity_key,
            entity_type=entity_type,
            tenant_id=tenant_id,
            category=category,
            deployment_key=deployment_key,
            form_key=form_key,
            resource_key=resource_key,
            batch_operation_type=batch_operation_type,
            process_definition_id=process_definition_id,
            job_key=job_key,
            user_task_key=user_task_key,
            decision_requirements_id=decision_requirements_id,
            decision_requirements_key=decision_requirements_key,
            decision_definition_id=decision_definition_id,
            decision_definition_key=decision_definition_key,
            decision_evaluation_key=decision_evaluation_key,
            related_entity_key=related_entity_key,
            related_entity_type=related_entity_type,
            entity_description=entity_description,
        )

        audit_log_search_query_request_filter.additional_properties = d
        return audit_log_search_query_request_filter

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
