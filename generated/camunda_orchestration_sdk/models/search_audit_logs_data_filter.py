from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import UserTaskKey, lift_user_task_key

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.actortype_exactmatch import ActortypeExactmatch
from ..models.batchoperationtype_exactmatch import BatchoperationtypeExactmatch
from ..models.category_exactmatch import CategoryExactmatch
from ..models.entitytype_exactmatch import EntitytypeExactmatch
from ..models.operationtype_exactmatch import OperationtypeExactmatch
from ..models.result_exactmatch import ResultExactmatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.actorid_advancedfilter import ActoridAdvancedfilter
    from ..models.actortype_advancedfilter import ActortypeAdvancedfilter
    from ..models.auditlogkey_advancedfilter import AuditlogkeyAdvancedfilter
    from ..models.batchoperationtype_advancedfilter import (
        BatchoperationtypeAdvancedfilter,
    )
    from ..models.category_advancedfilter import CategoryAdvancedfilter
    from ..models.decisiondefinitionkey_advancedfilter import (
        DecisiondefinitionkeyAdvancedfilter,
    )
    from ..models.decisionevaluationkey_advancedfilter import (
        DecisionevaluationkeyAdvancedfilter,
    )
    from ..models.decisionrequirementskey_advancedfilter import (
        DecisionrequirementskeyAdvancedfilter,
    )
    from ..models.deploymentkey_advancedfilter import DeploymentkeyAdvancedfilter
    from ..models.elementinstancekey_advancedfilter import (
        ElementinstancekeyAdvancedfilter,
    )
    from ..models.entitykey_advancedfilter import EntitykeyAdvancedfilter
    from ..models.entitytype_advancedfilter import EntitytypeAdvancedfilter
    from ..models.formkey_advancedfilter import FormkeyAdvancedfilter
    from ..models.jobkey_advancedfilter import JobkeyAdvancedfilter
    from ..models.operationtype_advancedfilter import OperationtypeAdvancedfilter
    from ..models.processdefinitionkey_advancedfilter import (
        ProcessdefinitionkeyAdvancedfilter,
    )
    from ..models.processinstancekey_advancedfilter import (
        ProcessinstancekeyAdvancedfilter,
    )
    from ..models.resourcekey_advancedfilter import ResourcekeyAdvancedfilter
    from ..models.result_advancedfilter import ResultAdvancedfilter
    from ..models.timestamp_advancedfilter import TimestampAdvancedfilter
    from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter


T = TypeVar("T", bound="SearchAuditLogsDataFilter")


@_attrs_define
class SearchAuditLogsDataFilter:
    """The audit log search filters.

    Attributes:
        audit_log_key (AuditlogkeyAdvancedfilter | str | Unset):
        process_definition_key (ProcessdefinitionkeyAdvancedfilter | str | Unset):
        process_instance_key (ProcessinstancekeyAdvancedfilter | str | Unset):
        element_instance_key (ElementinstancekeyAdvancedfilter | str | Unset):
        operation_type (OperationtypeAdvancedfilter | OperationtypeExactmatch | Unset):
        result (ResultAdvancedfilter | ResultExactmatch | Unset):
        timestamp (datetime.datetime | TimestampAdvancedfilter | Unset):
        actor_id (ActoridAdvancedfilter | str | Unset):
        actor_type (ActortypeAdvancedfilter | ActortypeExactmatch | Unset):
        entity_key (EntitykeyAdvancedfilter | str | Unset):
        entity_type (EntitytypeAdvancedfilter | EntitytypeExactmatch | Unset):
        tenant_id (ActoridAdvancedfilter | str | Unset):
        category (CategoryAdvancedfilter | CategoryExactmatch | Unset):
        deployment_key (DeploymentkeyAdvancedfilter | str | Unset):
        form_key (FormkeyAdvancedfilter | str | Unset):
        resource_key (ResourcekeyAdvancedfilter | str | Unset):
        batch_operation_type (BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset):
        process_definition_id (ActoridAdvancedfilter | str | Unset):
        job_key (JobkeyAdvancedfilter | str | Unset):
        user_task_key (str | Unset | UsertaskkeyAdvancedfilter):
        decision_requirements_id (ActoridAdvancedfilter | str | Unset):
        decision_requirements_key (DecisionrequirementskeyAdvancedfilter | str | Unset):
        decision_definition_id (ActoridAdvancedfilter | str | Unset):
        decision_definition_key (DecisiondefinitionkeyAdvancedfilter | str | Unset):
        decision_evaluation_key (DecisionevaluationkeyAdvancedfilter | str | Unset):
    """

    audit_log_key: AuditlogkeyAdvancedfilter | str | Unset = UNSET
    process_definition_key: ProcessdefinitionkeyAdvancedfilter | str | Unset = UNSET
    process_instance_key: ProcessinstancekeyAdvancedfilter | str | Unset = UNSET
    element_instance_key: ElementinstancekeyAdvancedfilter | str | Unset = UNSET
    operation_type: OperationtypeAdvancedfilter | OperationtypeExactmatch | Unset = (
        UNSET
    )
    result: ResultAdvancedfilter | ResultExactmatch | Unset = UNSET
    timestamp: datetime.datetime | TimestampAdvancedfilter | Unset = UNSET
    actor_id: ActoridAdvancedfilter | str | Unset = UNSET
    actor_type: ActortypeAdvancedfilter | ActortypeExactmatch | Unset = UNSET
    entity_key: EntitykeyAdvancedfilter | str | Unset = UNSET
    entity_type: EntitytypeAdvancedfilter | EntitytypeExactmatch | Unset = UNSET
    tenant_id: ActoridAdvancedfilter | str | Unset = UNSET
    category: CategoryAdvancedfilter | CategoryExactmatch | Unset = UNSET
    deployment_key: DeploymentkeyAdvancedfilter | str | Unset = UNSET
    form_key: FormkeyAdvancedfilter | str | Unset = UNSET
    resource_key: ResourcekeyAdvancedfilter | str | Unset = UNSET
    batch_operation_type: (
        BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset
    ) = UNSET
    process_definition_id: ActoridAdvancedfilter | str | Unset = UNSET
    job_key: JobkeyAdvancedfilter | str | Unset = UNSET
    user_task_key: UserTaskKey | Unset | UsertaskkeyAdvancedfilter = UNSET
    decision_requirements_id: ActoridAdvancedfilter | str | Unset = UNSET
    decision_requirements_key: DecisionrequirementskeyAdvancedfilter | str | Unset = (
        UNSET
    )
    decision_definition_id: ActoridAdvancedfilter | str | Unset = UNSET
    decision_definition_key: DecisiondefinitionkeyAdvancedfilter | str | Unset = UNSET
    decision_evaluation_key: DecisionevaluationkeyAdvancedfilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.actorid_advancedfilter import ActoridAdvancedfilter
        from ..models.auditlogkey_advancedfilter import AuditlogkeyAdvancedfilter
        from ..models.decisiondefinitionkey_advancedfilter import (
            DecisiondefinitionkeyAdvancedfilter,
        )
        from ..models.decisionevaluationkey_advancedfilter import (
            DecisionevaluationkeyAdvancedfilter,
        )
        from ..models.decisionrequirementskey_advancedfilter import (
            DecisionrequirementskeyAdvancedfilter,
        )
        from ..models.deploymentkey_advancedfilter import DeploymentkeyAdvancedfilter
        from ..models.elementinstancekey_advancedfilter import (
            ElementinstancekeyAdvancedfilter,
        )
        from ..models.entitykey_advancedfilter import EntitykeyAdvancedfilter
        from ..models.formkey_advancedfilter import FormkeyAdvancedfilter
        from ..models.jobkey_advancedfilter import JobkeyAdvancedfilter
        from ..models.processdefinitionkey_advancedfilter import (
            ProcessdefinitionkeyAdvancedfilter,
        )
        from ..models.processinstancekey_advancedfilter import (
            ProcessinstancekeyAdvancedfilter,
        )
        from ..models.resourcekey_advancedfilter import ResourcekeyAdvancedfilter
        from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter

        audit_log_key: dict[str, Any] | str | Unset
        if isinstance(self.audit_log_key, Unset):
            audit_log_key = UNSET
        elif isinstance(self.audit_log_key, AuditlogkeyAdvancedfilter):
            audit_log_key = self.audit_log_key.to_dict()
        else:
            audit_log_key = self.audit_log_key

        process_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_key, Unset):
            process_definition_key = UNSET
        elif isinstance(
            self.process_definition_key, ProcessdefinitionkeyAdvancedfilter
        ):
            process_definition_key = self.process_definition_key.to_dict()
        else:
            process_definition_key = self.process_definition_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, ProcessinstancekeyAdvancedfilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, ElementinstancekeyAdvancedfilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        operation_type: dict[str, Any] | str | Unset
        if isinstance(self.operation_type, Unset):
            operation_type = UNSET
        elif isinstance(self.operation_type, OperationtypeExactmatch):
            operation_type = self.operation_type.value
        else:
            operation_type = self.operation_type.to_dict()

        result: dict[str, Any] | str | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, ResultExactmatch):
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
        elif isinstance(self.actor_id, ActoridAdvancedfilter):
            actor_id = self.actor_id.to_dict()
        else:
            actor_id = self.actor_id

        actor_type: dict[str, Any] | str | Unset
        if isinstance(self.actor_type, Unset):
            actor_type = UNSET
        elif isinstance(self.actor_type, ActortypeExactmatch):
            actor_type = self.actor_type.value
        else:
            actor_type = self.actor_type.to_dict()

        entity_key: dict[str, Any] | str | Unset
        if isinstance(self.entity_key, Unset):
            entity_key = UNSET
        elif isinstance(self.entity_key, EntitykeyAdvancedfilter):
            entity_key = self.entity_key.to_dict()
        else:
            entity_key = self.entity_key

        entity_type: dict[str, Any] | str | Unset
        if isinstance(self.entity_type, Unset):
            entity_type = UNSET
        elif isinstance(self.entity_type, EntitytypeExactmatch):
            entity_type = self.entity_type.value
        else:
            entity_type = self.entity_type.to_dict()

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, ActoridAdvancedfilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        category: dict[str, Any] | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        elif isinstance(self.category, CategoryExactmatch):
            category = self.category.value
        else:
            category = self.category.to_dict()

        deployment_key: dict[str, Any] | str | Unset
        if isinstance(self.deployment_key, Unset):
            deployment_key = UNSET
        elif isinstance(self.deployment_key, DeploymentkeyAdvancedfilter):
            deployment_key = self.deployment_key.to_dict()
        else:
            deployment_key = self.deployment_key

        form_key: dict[str, Any] | str | Unset
        if isinstance(self.form_key, Unset):
            form_key = UNSET
        elif isinstance(self.form_key, FormkeyAdvancedfilter):
            form_key = self.form_key.to_dict()
        else:
            form_key = self.form_key

        resource_key: dict[str, Any] | str | Unset
        if isinstance(self.resource_key, Unset):
            resource_key = UNSET
        elif isinstance(self.resource_key, ResourcekeyAdvancedfilter):
            resource_key = self.resource_key.to_dict()
        else:
            resource_key = self.resource_key

        batch_operation_type: dict[str, Any] | str | Unset
        if isinstance(self.batch_operation_type, Unset):
            batch_operation_type = UNSET
        elif isinstance(self.batch_operation_type, BatchoperationtypeExactmatch):
            batch_operation_type = self.batch_operation_type.value
        else:
            batch_operation_type = self.batch_operation_type.to_dict()

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, ActoridAdvancedfilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        job_key: dict[str, Any] | str | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        elif isinstance(self.job_key, JobkeyAdvancedfilter):
            job_key = self.job_key.to_dict()
        else:
            job_key = self.job_key

        user_task_key: dict[str, Any] | str | Unset
        if isinstance(self.user_task_key, Unset):
            user_task_key = UNSET
        elif isinstance(self.user_task_key, UsertaskkeyAdvancedfilter):
            user_task_key = self.user_task_key.to_dict()
        else:
            user_task_key = self.user_task_key

        decision_requirements_id: dict[str, Any] | str | Unset
        if isinstance(self.decision_requirements_id, Unset):
            decision_requirements_id = UNSET
        elif isinstance(self.decision_requirements_id, ActoridAdvancedfilter):
            decision_requirements_id = self.decision_requirements_id.to_dict()
        else:
            decision_requirements_id = self.decision_requirements_id

        decision_requirements_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_requirements_key, Unset):
            decision_requirements_key = UNSET
        elif isinstance(
            self.decision_requirements_key, DecisionrequirementskeyAdvancedfilter
        ):
            decision_requirements_key = self.decision_requirements_key.to_dict()
        else:
            decision_requirements_key = self.decision_requirements_key

        decision_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.decision_definition_id, Unset):
            decision_definition_id = UNSET
        elif isinstance(self.decision_definition_id, ActoridAdvancedfilter):
            decision_definition_id = self.decision_definition_id.to_dict()
        else:
            decision_definition_id = self.decision_definition_id

        decision_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_definition_key, Unset):
            decision_definition_key = UNSET
        elif isinstance(
            self.decision_definition_key, DecisiondefinitionkeyAdvancedfilter
        ):
            decision_definition_key = self.decision_definition_key.to_dict()
        else:
            decision_definition_key = self.decision_definition_key

        decision_evaluation_key: dict[str, Any] | str | Unset
        if isinstance(self.decision_evaluation_key, Unset):
            decision_evaluation_key = UNSET
        elif isinstance(
            self.decision_evaluation_key, DecisionevaluationkeyAdvancedfilter
        ):
            decision_evaluation_key = self.decision_evaluation_key.to_dict()
        else:
            decision_evaluation_key = self.decision_evaluation_key

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.actorid_advancedfilter import ActoridAdvancedfilter
        from ..models.actortype_advancedfilter import ActortypeAdvancedfilter
        from ..models.auditlogkey_advancedfilter import AuditlogkeyAdvancedfilter
        from ..models.batchoperationtype_advancedfilter import (
            BatchoperationtypeAdvancedfilter,
        )
        from ..models.category_advancedfilter import CategoryAdvancedfilter
        from ..models.decisiondefinitionkey_advancedfilter import (
            DecisiondefinitionkeyAdvancedfilter,
        )
        from ..models.decisionevaluationkey_advancedfilter import (
            DecisionevaluationkeyAdvancedfilter,
        )
        from ..models.decisionrequirementskey_advancedfilter import (
            DecisionrequirementskeyAdvancedfilter,
        )
        from ..models.deploymentkey_advancedfilter import DeploymentkeyAdvancedfilter
        from ..models.elementinstancekey_advancedfilter import (
            ElementinstancekeyAdvancedfilter,
        )
        from ..models.entitykey_advancedfilter import EntitykeyAdvancedfilter
        from ..models.entitytype_advancedfilter import EntitytypeAdvancedfilter
        from ..models.formkey_advancedfilter import FormkeyAdvancedfilter
        from ..models.jobkey_advancedfilter import JobkeyAdvancedfilter
        from ..models.operationtype_advancedfilter import OperationtypeAdvancedfilter
        from ..models.processdefinitionkey_advancedfilter import (
            ProcessdefinitionkeyAdvancedfilter,
        )
        from ..models.processinstancekey_advancedfilter import (
            ProcessinstancekeyAdvancedfilter,
        )
        from ..models.resourcekey_advancedfilter import ResourcekeyAdvancedfilter
        from ..models.result_advancedfilter import ResultAdvancedfilter
        from ..models.timestamp_advancedfilter import TimestampAdvancedfilter
        from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter

        d = dict(src_dict)

        def _parse_audit_log_key(
            data: object,
        ) -> AuditlogkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                audit_log_key_type_1 = AuditlogkeyAdvancedfilter.from_dict(data)

                return audit_log_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuditlogkeyAdvancedfilter | str | Unset, data)

        audit_log_key = _parse_audit_log_key(d.pop("auditLogKey", UNSET))

        def _parse_process_definition_key(
            data: object,
        ) -> ProcessdefinitionkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_key_type_1 = (
                    ProcessdefinitionkeyAdvancedfilter.from_dict(data)
                )

                return process_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ProcessdefinitionkeyAdvancedfilter | str | Unset, data)

        process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey", UNSET)
        )

        def _parse_process_instance_key(
            data: object,
        ) -> ProcessinstancekeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_instance_key_type_1 = (
                    ProcessinstancekeyAdvancedfilter.from_dict(data)
                )

                return process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ProcessinstancekeyAdvancedfilter | str | Unset, data)

        process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey", UNSET)
        )

        def _parse_element_instance_key(
            data: object,
        ) -> ElementinstancekeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_instance_key_type_1 = (
                    ElementinstancekeyAdvancedfilter.from_dict(data)
                )

                return element_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ElementinstancekeyAdvancedfilter | str | Unset, data)

        element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey", UNSET)
        )

        def _parse_operation_type(
            data: object,
        ) -> OperationtypeAdvancedfilter | OperationtypeExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_type_type_0 = OperationtypeExactmatch(data)

                return operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            operation_type_type_1 = OperationtypeAdvancedfilter.from_dict(data)

            return operation_type_type_1

        operation_type = _parse_operation_type(d.pop("operationType", UNSET))

        def _parse_result(
            data: object,
        ) -> ResultAdvancedfilter | ResultExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_type_0 = ResultExactmatch(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            result_type_1 = ResultAdvancedfilter.from_dict(data)

            return result_type_1

        result = _parse_result(d.pop("result", UNSET))

        def _parse_timestamp(
            data: object,
        ) -> datetime.datetime | TimestampAdvancedfilter | Unset:
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
            timestamp_type_1 = TimestampAdvancedfilter.from_dict(data)

            return timestamp_type_1

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_actor_id(data: object) -> ActoridAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                actor_id_type_1 = ActoridAdvancedfilter.from_dict(data)

                return actor_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActoridAdvancedfilter | str | Unset, data)

        actor_id = _parse_actor_id(d.pop("actorId", UNSET))

        def _parse_actor_type(
            data: object,
        ) -> ActortypeAdvancedfilter | ActortypeExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actor_type_type_0 = ActortypeExactmatch(data)

                return actor_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            actor_type_type_1 = ActortypeAdvancedfilter.from_dict(data)

            return actor_type_type_1

        actor_type = _parse_actor_type(d.pop("actorType", UNSET))

        def _parse_entity_key(data: object) -> EntitykeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                entity_key_type_1 = EntitykeyAdvancedfilter.from_dict(data)

                return entity_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EntitykeyAdvancedfilter | str | Unset, data)

        entity_key = _parse_entity_key(d.pop("entityKey", UNSET))

        def _parse_entity_type(
            data: object,
        ) -> EntitytypeAdvancedfilter | EntitytypeExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_type_type_0 = EntitytypeExactmatch(data)

                return entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            entity_type_type_1 = EntitytypeAdvancedfilter.from_dict(data)

            return entity_type_type_1

        entity_type = _parse_entity_type(d.pop("entityType", UNSET))

        def _parse_tenant_id(data: object) -> ActoridAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                tenant_id_type_1 = ActoridAdvancedfilter.from_dict(data)

                return tenant_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActoridAdvancedfilter | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenantId", UNSET))

        def _parse_category(
            data: object,
        ) -> CategoryAdvancedfilter | CategoryExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                category_type_0 = CategoryExactmatch(data)

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            category_type_1 = CategoryAdvancedfilter.from_dict(data)

            return category_type_1

        category = _parse_category(d.pop("category", UNSET))

        def _parse_deployment_key(
            data: object,
        ) -> DeploymentkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                deployment_key_type_1 = DeploymentkeyAdvancedfilter.from_dict(data)

                return deployment_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeploymentkeyAdvancedfilter | str | Unset, data)

        deployment_key = _parse_deployment_key(d.pop("deploymentKey", UNSET))

        def _parse_form_key(data: object) -> FormkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                form_key_type_1 = FormkeyAdvancedfilter.from_dict(data)

                return form_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FormkeyAdvancedfilter | str | Unset, data)

        form_key = _parse_form_key(d.pop("formKey", UNSET))

        def _parse_resource_key(
            data: object,
        ) -> ResourcekeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                resource_key_type_1 = ResourcekeyAdvancedfilter.from_dict(data)

                return resource_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ResourcekeyAdvancedfilter | str | Unset, data)

        resource_key = _parse_resource_key(d.pop("resourceKey", UNSET))

        def _parse_batch_operation_type(
            data: object,
        ) -> BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                batch_operation_type_type_0 = BatchoperationtypeExactmatch(data)

                return batch_operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            batch_operation_type_type_1 = BatchoperationtypeAdvancedfilter.from_dict(
                data
            )

            return batch_operation_type_type_1

        batch_operation_type = _parse_batch_operation_type(
            d.pop("batchOperationType", UNSET)
        )

        def _parse_process_definition_id(
            data: object,
        ) -> ActoridAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_id_type_1 = ActoridAdvancedfilter.from_dict(data)

                return process_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActoridAdvancedfilter | str | Unset, data)

        process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId", UNSET)
        )

        def _parse_job_key(data: object) -> JobkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                job_key_type_1 = JobkeyAdvancedfilter.from_dict(data)

                return job_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobkeyAdvancedfilter | str | Unset, data)

        job_key = _parse_job_key(d.pop("jobKey", UNSET))

        def _parse_user_task_key(
            data: object,
        ) -> str | Unset | UsertaskkeyAdvancedfilter:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                user_task_key_type_1 = UsertaskkeyAdvancedfilter.from_dict(data)

                return user_task_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | Unset | UsertaskkeyAdvancedfilter, data)

        _raw_user_task_key = _parse_user_task_key(d.pop("userTaskKey", UNSET))

        user_task_key = (
            lift_user_task_key(_raw_user_task_key)
            if isinstance(_raw_user_task_key, str)
            else _raw_user_task_key
        )

        def _parse_decision_requirements_id(
            data: object,
        ) -> ActoridAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_requirements_id_type_1 = ActoridAdvancedfilter.from_dict(data)

                return decision_requirements_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActoridAdvancedfilter | str | Unset, data)

        decision_requirements_id = _parse_decision_requirements_id(
            d.pop("decisionRequirementsId", UNSET)
        )

        def _parse_decision_requirements_key(
            data: object,
        ) -> DecisionrequirementskeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_requirements_key_type_1 = (
                    DecisionrequirementskeyAdvancedfilter.from_dict(data)
                )

                return decision_requirements_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DecisionrequirementskeyAdvancedfilter | str | Unset, data)

        decision_requirements_key = _parse_decision_requirements_key(
            d.pop("decisionRequirementsKey", UNSET)
        )

        def _parse_decision_definition_id(
            data: object,
        ) -> ActoridAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_definition_id_type_1 = ActoridAdvancedfilter.from_dict(data)

                return decision_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActoridAdvancedfilter | str | Unset, data)

        decision_definition_id = _parse_decision_definition_id(
            d.pop("decisionDefinitionId", UNSET)
        )

        def _parse_decision_definition_key(
            data: object,
        ) -> DecisiondefinitionkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_definition_key_type_1 = (
                    DecisiondefinitionkeyAdvancedfilter.from_dict(data)
                )

                return decision_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DecisiondefinitionkeyAdvancedfilter | str | Unset, data)

        decision_definition_key = _parse_decision_definition_key(
            d.pop("decisionDefinitionKey", UNSET)
        )

        def _parse_decision_evaluation_key(
            data: object,
        ) -> DecisionevaluationkeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                decision_evaluation_key_type_1 = (
                    DecisionevaluationkeyAdvancedfilter.from_dict(data)
                )

                return decision_evaluation_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DecisionevaluationkeyAdvancedfilter | str | Unset, data)

        decision_evaluation_key = _parse_decision_evaluation_key(
            d.pop("decisionEvaluationKey", UNSET)
        )

        search_audit_logs_data_filter = cls(
            audit_log_key=audit_log_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            operation_type=operation_type,
            result=result,
            timestamp=timestamp,
            actor_id=actor_id,
            actor_type=actor_type,
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
        )

        search_audit_logs_data_filter.additional_properties = d
        return search_audit_logs_data_filter

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
