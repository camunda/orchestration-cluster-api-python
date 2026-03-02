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
    lift_element_id,
    lift_element_instance_key,
    lift_form_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
    lift_user_task_key,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_task_state_enum import UserTaskStateEnum
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders


T = TypeVar("T", bound="UserTaskResult")


@_attrs_define
class UserTaskResult:
    """
    Attributes:
        assignee (None | str): The assignee of the user task.
        candidate_groups (list[str]): The candidate groups for this user task.
        candidate_users (list[str]): The candidate users for this user task.
        completion_date (datetime.datetime | None): The completion date of a user task.
        follow_up_date (datetime.datetime | None): The follow date of a user task.
        due_date (datetime.datetime | None): The due date of a user task.
        external_form_reference (None | str): The external form reference.
        custom_headers (UserTaskResultCustomHeaders): Custom headers for the user task.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        form_key (None | str): The key of the form. Example: 2251799813684365.
        tags (list[str]): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or `.`;
            length ≤ 100. Example: ['high-touch', 'remediation'].
        name (str | Unset): The name for this user task.
        state (UserTaskStateEnum | Unset): The state of the user task.
            Note: FAILED state is only for legacy job-worker-based tasks.
        element_id (str | Unset): The element ID of the user task. Example: Activity_106kosb.
        process_definition_id (str | Unset): The ID of the process definition. Example: new-account-onboarding-workflow.
        creation_date (datetime.datetime | Unset): The creation date of a user task.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
        process_definition_version (int | Unset): The version of the process definition.
        priority (int | Unset): The priority of a user task. The higher the value the higher the priority. Default: 50.
        user_task_key (str | Unset): The key of the user task.
        element_instance_key (str | Unset): The key of the element instance. Example: 2251799813686789.
        process_name (None | str | Unset): The name of the process definition.
            This is `null` if the process has no name defined.
        process_definition_key (str | Unset): The key of the process definition. Example: 2251799813686749.
        process_instance_key (str | Unset): The key of the process instance. Example: 2251799813690746.
    """

    assignee: None | str
    candidate_groups: list[str]
    candidate_users: list[str]
    completion_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    due_date: datetime.datetime | None
    external_form_reference: None | str
    custom_headers: UserTaskResultCustomHeaders
    root_process_instance_key: None | ProcessInstanceKey
    form_key: None | FormKey
    tags: list[str]
    name: str | Unset = UNSET
    state: UserTaskStateEnum | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    creation_date: datetime.datetime | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    process_definition_version: int | Unset = UNSET
    priority: int | Unset = 50
    user_task_key: UserTaskKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    process_name: None | str | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        assignee: None | str
        assignee = self.assignee

        candidate_groups = self.candidate_groups

        candidate_users = self.candidate_users

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

        external_form_reference: None | str
        external_form_reference = self.external_form_reference

        custom_headers = self.custom_headers.to_dict()

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        form_key: None | FormKey
        form_key = self.form_key

        tags = self.tags

        name = self.name

        state: str | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        element_id = self.element_id

        process_definition_id = self.process_definition_id

        creation_date: str | Unset = UNSET
        if not isinstance(self.creation_date, Unset):
            creation_date = self.creation_date.isoformat()

        tenant_id = self.tenant_id

        process_definition_version = self.process_definition_version

        priority = self.priority

        user_task_key = self.user_task_key

        element_instance_key = self.element_instance_key

        process_name: None | str | Unset
        if isinstance(self.process_name, Unset):
            process_name = UNSET
        else:
            process_name = self.process_name

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assignee": assignee,
                "candidateGroups": candidate_groups,
                "candidateUsers": candidate_users,
                "completionDate": completion_date,
                "followUpDate": follow_up_date,
                "dueDate": due_date,
                "externalFormReference": external_form_reference,
                "customHeaders": custom_headers,
                "rootProcessInstanceKey": root_process_instance_key,
                "formKey": form_key,
                "tags": tags,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if state is not UNSET:
            field_dict["state"] = state
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if process_definition_version is not UNSET:
            field_dict["processDefinitionVersion"] = process_definition_version
        if priority is not UNSET:
            field_dict["priority"] = priority
        if user_task_key is not UNSET:
            field_dict["userTaskKey"] = user_task_key
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders

        d = dict(src_dict)

        def _parse_assignee(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        assignee = _parse_assignee(d.pop("assignee"))

        candidate_groups = cast(list[str], d.pop("candidateGroups"))

        candidate_users = cast(list[str], d.pop("candidateUsers"))

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

        def _parse_external_form_reference(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_form_reference = _parse_external_form_reference(
            d.pop("externalFormReference")
        )

        custom_headers = UserTaskResultCustomHeaders.from_dict(d.pop("customHeaders"))

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

        def _parse_form_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_form_key = _parse_form_key(d.pop("formKey"))

        form_key = (
            lift_form_key(_raw_form_key)
            if isinstance(_raw_form_key, str)
            else _raw_form_key
        )

        tags = cast(list[str], d.pop("tags"))

        name = d.pop("name", UNSET)

        _state = d.pop("state", UNSET)
        state: UserTaskStateEnum | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = UserTaskStateEnum(_state)

        element_id = (
            lift_element_id(_val)
            if (_val := d.pop("elementId", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_id = (
            lift_process_definition_id(_val)
            if (_val := d.pop("processDefinitionId", UNSET)) is not UNSET
            else UNSET
        )

        _creation_date = d.pop("creationDate", UNSET)
        creation_date: datetime.datetime | Unset
        if isinstance(_creation_date, Unset):
            creation_date = UNSET
        else:
            creation_date = isoparse(_creation_date)

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        process_definition_version = d.pop("processDefinitionVersion", UNSET)

        priority = d.pop("priority", UNSET)

        user_task_key = (
            lift_user_task_key(_val)
            if (_val := d.pop("userTaskKey", UNSET)) is not UNSET
            else UNSET
        )

        element_instance_key = (
            lift_element_instance_key(_val)
            if (_val := d.pop("elementInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        def _parse_process_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        process_name = _parse_process_name(d.pop("processName", UNSET))

        process_definition_key = (
            lift_process_definition_key(_val)
            if (_val := d.pop("processDefinitionKey", UNSET)) is not UNSET
            else UNSET
        )

        process_instance_key = (
            lift_process_instance_key(_val)
            if (_val := d.pop("processInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        user_task_result = cls(
            assignee=assignee,
            candidate_groups=candidate_groups,
            candidate_users=candidate_users,
            completion_date=completion_date,
            follow_up_date=follow_up_date,
            due_date=due_date,
            external_form_reference=external_form_reference,
            custom_headers=custom_headers,
            root_process_instance_key=root_process_instance_key,
            form_key=form_key,
            tags=tags,
            name=name,
            state=state,
            element_id=element_id,
            process_definition_id=process_definition_id,
            creation_date=creation_date,
            tenant_id=tenant_id,
            process_definition_version=process_definition_version,
            priority=priority,
            user_task_key=user_task_key,
            element_instance_key=element_instance_key,
            process_name=process_name,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
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
