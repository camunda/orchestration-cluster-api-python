from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    FormKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    UserTaskKey,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_task_state_enum import UserTaskStateEnum

if TYPE_CHECKING:
    from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders


T = TypeVar("T", bound="UserTaskResult")


@_attrs_define
class UserTaskResult:
    """
    Attributes:
        name (None | str): The name for this user task.
        state (UserTaskStateEnum): The state of the user task.
            Note: FAILED state is only for legacy job-worker-based tasks.
        assignee (None | str): The assignee of the user task.
        element_id (str): The element ID of the user task. Example: Activity_106kosb.
        candidate_groups (list[str]): The candidate groups for this user task.
        candidate_users (list[str]): The candidate users for this user task.
        process_definition_id (str): The ID of the process definition. Example: new-account-onboarding-workflow.
        creation_date (datetime.datetime): The creation date of a user task.
        completion_date (datetime.datetime | None): The completion date of a user task.
        follow_up_date (datetime.datetime | None): The follow date of a user task.
        due_date (datetime.datetime | None): The due date of a user task.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        external_form_reference (None | str): The external form reference.
        process_definition_version (int): The version of the process definition.
        custom_headers (UserTaskResultCustomHeaders): Custom headers for the user task.
        priority (int): The priority of a user task. The higher the value the higher the priority. Default: 50.
        user_task_key (str): The key of the user task.
        element_instance_key (str): The key of the element instance. Example: 2251799813686789.
        process_name (None | str): The name of the process definition.
            This is `null` if the process has no name defined.
        process_definition_key (str): The key of the process definition. Example: 2251799813686749.
        process_instance_key (str): The key of the process instance. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        form_key (None | str): The key of the form. Example: 2251799813684365.
        tags (list[str]): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or `.`;
            length ≤ 100. Example: ['high-touch', 'remediation'].
    """

    name: None | str
    state: UserTaskStateEnum
    assignee: None | str
    element_id: ElementId
    candidate_groups: list[str]
    candidate_users: list[str]
    process_definition_id: ProcessDefinitionId
    creation_date: datetime.datetime
    completion_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    due_date: datetime.datetime | None
    tenant_id: TenantId
    external_form_reference: None | str
    process_definition_version: int
    custom_headers: UserTaskResultCustomHeaders
    user_task_key: UserTaskKey
    element_instance_key: ElementInstanceKey
    process_name: None | str
    process_definition_key: ProcessDefinitionKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    form_key: None | FormKey
    tags: list[str]
    priority: int = 50
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        name: None | str
        name = self.name

        state = self.state.value

        assignee: None | str
        assignee = self.assignee

        element_id = self.element_id

        candidate_groups = self.candidate_groups

        candidate_users = self.candidate_users

        process_definition_id = self.process_definition_id

        creation_date = self.creation_date.isoformat()

        completion_date: None | str
        if isinstance(self.completion_date, datetime.datetime):
            completion_date = self.completion_date.isoformat()
        else:
            completion_date = self.completion_date

        follow_up_date: None | str
        if isinstance(self.follow_up_date, datetime.datetime):
            follow_up_date = self.follow_up_date.isoformat()
        else:
            follow_up_date = self.follow_up_date

        due_date: None | str
        if isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        tenant_id = self.tenant_id

        external_form_reference: None | str
        external_form_reference = self.external_form_reference

        process_definition_version = self.process_definition_version

        custom_headers = self.custom_headers.to_dict()

        priority = self.priority

        user_task_key = self.user_task_key

        element_instance_key = self.element_instance_key

        process_name: None | str
        process_name = self.process_name

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        form_key: None | FormKey
        form_key = self.form_key

        tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "state": state,
                "assignee": assignee,
                "elementId": element_id,
                "candidateGroups": candidate_groups,
                "candidateUsers": candidate_users,
                "processDefinitionId": process_definition_id,
                "creationDate": creation_date,
                "completionDate": completion_date,
                "followUpDate": follow_up_date,
                "dueDate": due_date,
                "tenantId": tenant_id,
                "externalFormReference": external_form_reference,
                "processDefinitionVersion": process_definition_version,
                "customHeaders": custom_headers,
                "priority": priority,
                "userTaskKey": user_task_key,
                "elementInstanceKey": element_instance_key,
                "processName": process_name,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "formKey": form_key,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        state = UserTaskStateEnum(d.pop("state"))

        def _parse_assignee(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        assignee = _parse_assignee(d.pop("assignee"))

        element_id = ElementId(d.pop("elementId"))

        candidate_groups = cast(list[str], d.pop("candidateGroups"))

        candidate_users = cast(list[str], d.pop("candidateUsers"))

        process_definition_id = ProcessDefinitionId(d.pop("processDefinitionId"))

        creation_date = isoparse(d.pop("creationDate"))

        def _parse_completion_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completion_date_type_0 = isoparse(data)

                return completion_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completion_date = _parse_completion_date(d.pop("completionDate"))

        def _parse_follow_up_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                follow_up_date_type_0 = isoparse(data)

                return follow_up_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        follow_up_date = _parse_follow_up_date(d.pop("followUpDate"))

        def _parse_due_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data)

                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        due_date = _parse_due_date(d.pop("dueDate"))

        tenant_id = TenantId(d.pop("tenantId"))

        def _parse_external_form_reference(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_form_reference = _parse_external_form_reference(
            d.pop("externalFormReference")
        )

        process_definition_version = d.pop("processDefinitionVersion")

        custom_headers = UserTaskResultCustomHeaders.from_dict(d.pop("customHeaders"))

        priority = d.pop("priority")

        user_task_key = UserTaskKey(d.pop("userTaskKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        def _parse_process_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        process_name = _parse_process_name(d.pop("processName"))

        process_definition_key = ProcessDefinitionKey(d.pop("processDefinitionKey"))

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

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

        def _parse_form_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_form_key = _parse_form_key(d.pop("formKey"))

        form_key = (
            FormKey(_raw_form_key) if isinstance(_raw_form_key, str) else _raw_form_key
        )

        tags = cast(list[str], d.pop("tags"))

        user_task_result = cls(
            name=name,
            state=state,
            assignee=assignee,
            element_id=element_id,
            candidate_groups=candidate_groups,
            candidate_users=candidate_users,
            process_definition_id=process_definition_id,
            creation_date=creation_date,
            completion_date=completion_date,
            follow_up_date=follow_up_date,
            due_date=due_date,
            tenant_id=tenant_id,
            external_form_reference=external_form_reference,
            process_definition_version=process_definition_version,
            custom_headers=custom_headers,
            priority=priority,
            user_task_key=user_task_key,
            element_instance_key=element_instance_key,
            process_name=process_name,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            form_key=form_key,
            tags=tags,
        )

        user_task_result.additional_properties = d
        return user_task_result

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
