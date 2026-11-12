from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    AuditLogEntityKey,
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
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_log_category_enum import AuditLogCategoryEnum
from ..models.audit_log_entity_type_enum import AuditLogEntityTypeEnum
from ..models.audit_log_operation_type_enum import AuditLogOperationTypeEnum
from ..models.audit_log_result_actor_type import AuditLogResultActorType
from ..models.audit_log_result_batch_operation_type import (
    AuditLogResultBatchOperationType,
)
from ..models.audit_log_result_enum import AuditLogResultEnum
from ..models.audit_log_result_related_entity_type import (
    AuditLogResultRelatedEntityType,
)

T = TypeVar("T", bound="AuditLogResult")


@_attrs_define
class AuditLogResult:
    """Audit log item.

    Attributes:
        audit_log_key (str): The unique key of the audit log entry. Example: 22517998136843567.
        entity_key (str): System-generated entity key for an audit log entry. Example: 22517998136843567.
        entity_type (AuditLogEntityTypeEnum): The type of entity affected by the operation.
        operation_type (AuditLogOperationTypeEnum): The type of operation performed.
        batch_operation_key (None | str): Key of the batch operation. Example: 2251799813684321.
        batch_operation_type (AuditLogResultBatchOperationType): The type of batch operation performed, if this is part
            of a batch.
        timestamp (datetime.datetime): The timestamp when the operation occurred.
        actor_id (None | str): The ID of the actor who performed the operation.
        actor_type (AuditLogResultActorType): The type of the actor who performed the operation.
        agent_element_id (None | str): The element ID of the agent that performed the operation (e.g. ad-hoc subprocess
            element ID).
        tenant_id (None | str): The tenant ID of the audit log. Example: customer-service.
        result (AuditLogResultEnum): The result status of the operation.
        category (AuditLogCategoryEnum): The category of the audit log operation.
        process_definition_id (None | str): The process definition ID. Example: new-account-onboarding-workflow.
        process_definition_key (None | str): The key of the process definition. Example: 2251799813686749.
        process_instance_key (None | str): The key of the process instance. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        element_instance_key (None | str): The key of the element instance. Example: 2251799813686789.
        job_key (None | str): The key of the job. Example: 2251799813653498.
        user_task_key (None | str): The key of the user task.
        decision_requirements_id (None | str): The decision requirements ID.
        decision_requirements_key (None | str): The assigned key of the decision requirements. Example:
            2251799813683346.
        decision_definition_id (None | str): The decision definition ID. Example: new-hire-onboarding-workflow.
        decision_definition_key (None | str): The key of the decision definition. Example: 2251799813326547.
        decision_evaluation_key (None | str): The key of the decision evaluation. Example: 2251792362345323.
        deployment_key (None | str): The key of the deployment.
        form_key (None | str): The key of the form. Example: 2251799813684365.
        resource_key (str): The system-assigned key for this resource.
        related_entity_key (None | str): The key of the related entity. The content depends on the operation type and
            entity type.
            For example, for authorization operations, this will contain the ID of the owner (e.g., user or group) the
            authorization belongs to.
             Example: 22517998136843567.
        related_entity_type (AuditLogResultRelatedEntityType): The type of the related entity. The content depends on
            the operation type and entity type.
            For example, for authorization operations, this will contain the type of the owner (e.g., USER or GROUP) the
            authorization belongs to.
        entity_description (None | str): Additional description of the entity affected by the operation.
            For example, for variable operations, this will contain the variable name.
    """

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
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        audit_log_key = self.audit_log_key

        entity_key = self.entity_key

        entity_type = self.entity_type.value

        operation_type = self.operation_type.value

        batch_operation_key: None | BatchOperationKey
        batch_operation_key = self.batch_operation_key

        batch_operation_type = self.batch_operation_type.value

        timestamp = self.timestamp.isoformat()

        actor_id: None | str
        actor_id = self.actor_id

        actor_type = self.actor_type.value

        agent_element_id: None | str
        agent_element_id = self.agent_element_id

        tenant_id: None | TenantId
        tenant_id = self.tenant_id

        result = self.result.value

        category = self.category.value

        process_definition_id: None | ProcessDefinitionId
        process_definition_id = self.process_definition_id

        process_definition_key: None | ProcessDefinitionKey
        process_definition_key = self.process_definition_key

        process_instance_key: None | ProcessInstanceKey
        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        element_instance_key: None | ElementInstanceKey
        element_instance_key = self.element_instance_key

        job_key: None | JobKey
        job_key = self.job_key

        user_task_key: None | UserTaskKey
        user_task_key = self.user_task_key

        decision_requirements_id: None | str
        decision_requirements_id = self.decision_requirements_id

        decision_requirements_key: None | DecisionRequirementsKey
        decision_requirements_key = self.decision_requirements_key

        decision_definition_id: None | DecisionDefinitionId
        decision_definition_id = self.decision_definition_id

        decision_definition_key: None | DecisionDefinitionKey
        decision_definition_key = self.decision_definition_key

        decision_evaluation_key: None | DecisionEvaluationKey
        decision_evaluation_key = self.decision_evaluation_key

        deployment_key: None | DeploymentKey
        deployment_key = self.deployment_key

        form_key: None | FormKey
        form_key = self.form_key

        resource_key: str
        resource_key = self.resource_key

        related_entity_key: None | AuditLogEntityKey
        related_entity_key = self.related_entity_key

        related_entity_type = self.related_entity_type.value

        entity_description: None | str
        entity_description = self.entity_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auditLogKey": audit_log_key,
                "entityKey": entity_key,
                "entityType": entity_type,
                "operationType": operation_type,
                "batchOperationKey": batch_operation_key,
                "batchOperationType": batch_operation_type,
                "timestamp": timestamp,
                "actorId": actor_id,
                "actorType": actor_type,
                "agentElementId": agent_element_id,
                "tenantId": tenant_id,
                "result": result,
                "category": category,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "elementInstanceKey": element_instance_key,
                "jobKey": job_key,
                "userTaskKey": user_task_key,
                "decisionRequirementsId": decision_requirements_id,
                "decisionRequirementsKey": decision_requirements_key,
                "decisionDefinitionId": decision_definition_id,
                "decisionDefinitionKey": decision_definition_key,
                "decisionEvaluationKey": decision_evaluation_key,
                "deploymentKey": deployment_key,
                "formKey": form_key,
                "resourceKey": resource_key,
                "relatedEntityKey": related_entity_key,
                "relatedEntityType": related_entity_type,
                "entityDescription": entity_description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        audit_log_key = AuditLogKey(d.pop("auditLogKey"))

        entity_key = d.pop("entityKey")

        entity_type = AuditLogEntityTypeEnum(d.pop("entityType"))

        operation_type = AuditLogOperationTypeEnum(d.pop("operationType"))

        def _parse_batch_operation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_batch_operation_key = _parse_batch_operation_key(
            d.pop("batchOperationKey")
        )

        batch_operation_key = (
            BatchOperationKey(_raw_batch_operation_key)
            if isinstance(_raw_batch_operation_key, str)
            else _raw_batch_operation_key
        )

        batch_operation_type = AuditLogResultBatchOperationType(
            d.pop("batchOperationType")
        )

        timestamp = isoparse(d.pop("timestamp"))

        def _parse_actor_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_id = _parse_actor_id(d.pop("actorId"))

        actor_type = AuditLogResultActorType(d.pop("actorType"))

        def _parse_agent_element_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        agent_element_id = _parse_agent_element_id(d.pop("agentElementId"))

        def _parse_tenant_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_tenant_id = _parse_tenant_id(d.pop("tenantId"))

        tenant_id = (
            TenantId(_raw_tenant_id)
            if isinstance(_raw_tenant_id, str)
            else _raw_tenant_id
        )

        result = AuditLogResultEnum(d.pop("result"))

        category = AuditLogCategoryEnum(d.pop("category"))

        def _parse_process_definition_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId")
        )

        process_definition_id = (
            ProcessDefinitionId(_raw_process_definition_id)
            if isinstance(_raw_process_definition_id, str)
            else _raw_process_definition_id
        )

        def _parse_process_definition_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_definition_key = (
            ProcessDefinitionKey(_raw_process_definition_key)
            if isinstance(_raw_process_definition_key, str)
            else _raw_process_definition_key
        )

        def _parse_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey")
        )

        process_instance_key = (
            ProcessInstanceKey(_raw_process_instance_key)
            if isinstance(_raw_process_instance_key, str)
            else _raw_process_instance_key
        )

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey")
        )

        element_instance_key = (
            ElementInstanceKey(_raw_element_instance_key)
            if isinstance(_raw_element_instance_key, str)
            else _raw_element_instance_key
        )

        def _parse_job_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_job_key = _parse_job_key(d.pop("jobKey"))

        job_key = (
            JobKey(_raw_job_key) if isinstance(_raw_job_key, str) else _raw_job_key
        )

        def _parse_user_task_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_user_task_key = _parse_user_task_key(d.pop("userTaskKey"))

        user_task_key = (
            UserTaskKey(_raw_user_task_key)
            if isinstance(_raw_user_task_key, str)
            else _raw_user_task_key
        )

        def _parse_decision_requirements_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        decision_requirements_id = _parse_decision_requirements_id(
            d.pop("decisionRequirementsId")
        )

        def _parse_decision_requirements_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_decision_requirements_key = _parse_decision_requirements_key(
            d.pop("decisionRequirementsKey")
        )

        decision_requirements_key = (
            DecisionRequirementsKey(_raw_decision_requirements_key)
            if isinstance(_raw_decision_requirements_key, str)
            else _raw_decision_requirements_key
        )

        def _parse_decision_definition_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_decision_definition_id = _parse_decision_definition_id(
            d.pop("decisionDefinitionId")
        )

        decision_definition_id = (
            DecisionDefinitionId(_raw_decision_definition_id)
            if isinstance(_raw_decision_definition_id, str)
            else _raw_decision_definition_id
        )

        def _parse_decision_definition_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_decision_definition_key = _parse_decision_definition_key(
            d.pop("decisionDefinitionKey")
        )

        decision_definition_key = (
            DecisionDefinitionKey(_raw_decision_definition_key)
            if isinstance(_raw_decision_definition_key, str)
            else _raw_decision_definition_key
        )

        def _parse_decision_evaluation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_decision_evaluation_key = _parse_decision_evaluation_key(
            d.pop("decisionEvaluationKey")
        )

        decision_evaluation_key = (
            DecisionEvaluationKey(_raw_decision_evaluation_key)
            if isinstance(_raw_decision_evaluation_key, str)
            else _raw_decision_evaluation_key
        )

        def _parse_deployment_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_deployment_key = _parse_deployment_key(d.pop("deploymentKey"))

        deployment_key = (
            DeploymentKey(_raw_deployment_key)
            if isinstance(_raw_deployment_key, str)
            else _raw_deployment_key
        )

        def _parse_form_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_form_key = _parse_form_key(d.pop("formKey"))

        form_key = (
            FormKey(_raw_form_key) if isinstance(_raw_form_key, str) else _raw_form_key
        )

        def _parse_resource_key(data: object) -> str:
            return cast(str, data)

        resource_key = _parse_resource_key(d.pop("resourceKey"))

        def _parse_related_entity_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_related_entity_key = _parse_related_entity_key(d.pop("relatedEntityKey"))

        related_entity_key = (
            AuditLogEntityKey(_raw_related_entity_key)
            if isinstance(_raw_related_entity_key, str)
            else _raw_related_entity_key
        )

        related_entity_type = AuditLogResultRelatedEntityType(
            d.pop("relatedEntityType")
        )

        def _parse_entity_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        entity_description = _parse_entity_description(d.pop("entityDescription"))

        audit_log_result = cls(
            audit_log_key=audit_log_key,
            entity_key=entity_key,
            entity_type=entity_type,
            operation_type=operation_type,
            batch_operation_key=batch_operation_key,
            batch_operation_type=batch_operation_type,
            timestamp=timestamp,
            actor_id=actor_id,
            actor_type=actor_type,
            agent_element_id=agent_element_id,
            tenant_id=tenant_id,
            result=result,
            category=category,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            element_instance_key=element_instance_key,
            job_key=job_key,
            user_task_key=user_task_key,
            decision_requirements_id=decision_requirements_id,
            decision_requirements_key=decision_requirements_key,
            decision_definition_id=decision_definition_id,
            decision_definition_key=decision_definition_key,
            decision_evaluation_key=decision_evaluation_key,
            deployment_key=deployment_key,
            form_key=form_key,
            resource_key=resource_key,
            related_entity_key=related_entity_key,
            related_entity_type=related_entity_type,
            entity_description=entity_description,
        )

        audit_log_result.additional_properties = d
        return audit_log_result

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
