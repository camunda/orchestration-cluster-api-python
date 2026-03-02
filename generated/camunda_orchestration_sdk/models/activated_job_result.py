from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    lift_element_id,
    lift_element_instance_key,
    lift_job_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_kind_enum import JobKindEnum
from ..models.job_listener_event_type_enum import JobListenerEventTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.activated_job_result_custom_headers import (
        ActivatedJobResultCustomHeaders,
    )
    from ..models.activated_job_result_user_task import ActivatedJobResultUserTask
    from ..models.activated_job_result_variables import ActivatedJobResultVariables


T = TypeVar("T", bound="ActivatedJobResult")


@_attrs_define
class ActivatedJobResult:
    """
    Attributes:
        type_ (str): The type of the job (should match what was requested). Example: create-new-user-record.
        process_definition_id (str): The bpmn process ID of the job's process definition. Example: new-account-
            onboarding-workflow.
        process_definition_version (int): The version of the job's process definition. Example: 1.
        element_id (str): The associated task element ID. Example: Activity_106kosb.
        custom_headers (ActivatedJobResultCustomHeaders): A set of custom headers defined during modelling; returned as
            a serialized JSON document.
        worker (str): The name of the worker which activated this job. Example: worker-324.
        retries (int): The amount of retries left to this job (should always be positive). Example: 3.
        deadline (int): When the job can be activated again, sent as a UNIX epoch timestamp. Example: 1757280974277.
        variables (ActivatedJobResultVariables): All variables visible to the task scope, computed at activation time.
        tenant_id (str): The ID of the tenant that owns the job. Example: customer-service.
        job_key (str): The key, a unique identifier for the job. Example: 2251799813653498.
        process_instance_key (str): The job's process instance key. Example: 2251799813690746.
        process_definition_key (str): The key of the job's process definition. Example: 2251799813686749.
        element_instance_key (str): The element instance key of the task. Example: 2251799813686789.
        kind (JobKindEnum): The job kind. Example: BPMN_ELEMENT.
        listener_event_type (JobListenerEventTypeEnum): The listener event type of the job. Example: UNSPECIFIED.
        tags (list[str]): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or `.`;
            length ≤ 100. Example: ['high-touch', 'remediation'].
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        user_task (ActivatedJobResultUserTask | None | Unset): User task properties, if the job is a user task.
            This is `null` if the job is not a user task.
    """

    type_: str
    process_definition_id: ProcessDefinitionId
    process_definition_version: int
    element_id: ElementId
    custom_headers: ActivatedJobResultCustomHeaders
    worker: str
    retries: int
    deadline: int
    variables: ActivatedJobResultVariables
    tenant_id: TenantId
    job_key: JobKey
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    element_instance_key: ElementInstanceKey
    kind: JobKindEnum
    listener_event_type: JobListenerEventTypeEnum
    tags: list[str]
    root_process_instance_key: None | ProcessInstanceKey
    user_task: ActivatedJobResultUserTask | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.activated_job_result_user_task import ActivatedJobResultUserTask

        type_ = self.type_

        process_definition_id = self.process_definition_id

        process_definition_version = self.process_definition_version

        element_id = self.element_id

        custom_headers = self.custom_headers.to_dict()

        worker = self.worker

        retries = self.retries

        deadline = self.deadline

        variables = self.variables.to_dict()

        tenant_id = self.tenant_id

        job_key = self.job_key

        process_instance_key = self.process_instance_key

        process_definition_key = self.process_definition_key

        element_instance_key = self.element_instance_key

        kind = self.kind.value

        listener_event_type = self.listener_event_type.value

        tags = self.tags

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        user_task: dict[str, Any] | None | Unset
        if isinstance(self.user_task, Unset):
            user_task = UNSET
        elif isinstance(self.user_task, ActivatedJobResultUserTask):
            user_task = self.user_task.to_dict()
        else:
            user_task = self.user_task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "processDefinitionId": process_definition_id,
                "processDefinitionVersion": process_definition_version,
                "elementId": element_id,
                "customHeaders": custom_headers,
                "worker": worker,
                "retries": retries,
                "deadline": deadline,
                "variables": variables,
                "tenantId": tenant_id,
                "jobKey": job_key,
                "processInstanceKey": process_instance_key,
                "processDefinitionKey": process_definition_key,
                "elementInstanceKey": element_instance_key,
                "kind": kind,
                "listenerEventType": listener_event_type,
                "tags": tags,
                "rootProcessInstanceKey": root_process_instance_key,
            }
        )
        if user_task is not UNSET:
            field_dict["userTask"] = user_task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activated_job_result_custom_headers import (
            ActivatedJobResultCustomHeaders,
        )
        from ..models.activated_job_result_user_task import ActivatedJobResultUserTask
        from ..models.activated_job_result_variables import ActivatedJobResultVariables

        d = dict(src_dict)
        type_ = d.pop("type")

        process_definition_id = lift_process_definition_id(d.pop("processDefinitionId"))

        process_definition_version = d.pop("processDefinitionVersion")

        element_id = lift_element_id(d.pop("elementId"))

        custom_headers = ActivatedJobResultCustomHeaders.from_dict(
            d.pop("customHeaders")
        )

        worker = d.pop("worker")

        retries = d.pop("retries")

        deadline = d.pop("deadline")

        variables = ActivatedJobResultVariables.from_dict(d.pop("variables"))

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        job_key = lift_job_key(d.pop("jobKey"))

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        element_instance_key = lift_element_instance_key(d.pop("elementInstanceKey"))

        kind = JobKindEnum(d.pop("kind"))

        listener_event_type = JobListenerEventTypeEnum(d.pop("listenerEventType"))

        tags = cast(list[str], d.pop("tags"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            lift_process_instance_key(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        def _parse_user_task(data: object) -> ActivatedJobResultUserTask | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_activated_job_result_user_task_type_0 = (
                    ActivatedJobResultUserTask.from_dict(data)
                )

                return componentsschemas_activated_job_result_user_task_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActivatedJobResultUserTask | None | Unset, data)

        user_task = _parse_user_task(d.pop("userTask", UNSET))

        activated_job_result = cls(
            type_=type_,
            process_definition_id=process_definition_id,
            process_definition_version=process_definition_version,
            element_id=element_id,
            custom_headers=custom_headers,
            worker=worker,
            retries=retries,
            deadline=deadline,
            variables=variables,
            tenant_id=tenant_id,
            job_key=job_key,
            process_instance_key=process_instance_key,
            process_definition_key=process_definition_key,
            element_instance_key=element_instance_key,
            kind=kind,
            listener_event_type=listener_event_type,
            tags=tags,
            root_process_instance_key=root_process_instance_key,
            user_task=user_task,
        )

        activated_job_result.additional_properties = d
        return activated_job_result

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
