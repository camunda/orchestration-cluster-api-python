from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import (
    BusinessId,
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

from ..models.user_task_lookup_state_enum import UserTaskLookupStateEnum

if TYPE_CHECKING:
    from ..models.user_task_lookup_result_variables import UserTaskLookupResultVariables
    from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders


T = TypeVar("T", bound="UserTaskLookupResult")


@_attrs_define
class UserTaskLookupResult:
    """
    Attributes:
        user_task_key (str): The key of the user task.
        state (UserTaskLookupStateEnum): The lifecycle state of an active user task. A state ending in `-ING` means a
            change to the
            task is in progress, for example waiting for task listeners; the task fields still hold
            the values from before the change.
        element_id (str): The element ID of the user task. Example: Activity_106kosb.
        element_instance_key (str): The key of the element instance. Example: 2251799813686789.
        process_instance_key (str): The key of the process instance. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        process_definition_id (str): The ID of the process definition. Example: new-account-onboarding-workflow.
        process_definition_key (str): The key of the process definition. Example: 2251799813686749.
        process_definition_version (int): The version of the process definition.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        assignee (None | str): The assignee of the user task. While the task is in the `CREATING` state, the assignee
            from the process model is not set yet.
        candidate_groups (list[str]): The candidate groups for this user task.
        candidate_users (list[str]): The candidate users for this user task.
        due_date (datetime.datetime | None): The due date of the user task.
        follow_up_date (datetime.datetime | None): The follow-up date of the user task.
        form_key (None | str): The key of the form. Example: 2251799813684365.
        external_form_reference (None | str): The external form reference.
        custom_headers (UserTaskResultCustomHeaders): Custom headers for the user task.
        priority (int): The priority of the user task. The higher the value the higher the priority.
        tags (list[str]): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or `.`;
            length ≤ 100. Example: ['high-touch', 'remediation'].
        business_id (None | str): The business ID of the owning process instance, inherited when the user task was
            created. This is `null` for user tasks whose owning process instance has no business ID.
             Example: order-12345.
        creation_date (datetime.datetime): The creation date of the user task.
        variables (UserTaskLookupResultVariables): The variables visible to the user task, as a JSON object of name and
            value. If a name exists in several scopes, the value of the innermost scope is returned. Values are never
            truncated.
    """

    user_task_key: UserTaskKey
    state: UserTaskLookupStateEnum
    element_id: ElementId
    element_instance_key: ElementInstanceKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    process_definition_id: ProcessDefinitionId
    process_definition_key: ProcessDefinitionKey
    process_definition_version: int
    tenant_id: TenantId
    assignee: None | str
    candidate_groups: list[str]
    candidate_users: list[str]
    due_date: datetime.datetime | None
    follow_up_date: datetime.datetime | None
    form_key: None | FormKey
    external_form_reference: None | str
    custom_headers: UserTaskResultCustomHeaders
    priority: int
    tags: list[str]
    business_id: None | BusinessId
    creation_date: datetime.datetime
    variables: UserTaskLookupResultVariables
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        user_task_key = self.user_task_key

        state = self.state.value

        element_id = self.element_id

        element_instance_key = self.element_instance_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_definition_id = self.process_definition_id

        process_definition_key = self.process_definition_key

        process_definition_version = self.process_definition_version

        tenant_id = self.tenant_id

        assignee: None | str
        assignee = self.assignee

        candidate_groups = self.candidate_groups

        candidate_users = self.candidate_users

        due_date: None | str
        if isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        follow_up_date: None | str
        if isinstance(self.follow_up_date, datetime.datetime):
            follow_up_date = self.follow_up_date.isoformat()
        else:
            follow_up_date = self.follow_up_date

        form_key: None | FormKey
        form_key = self.form_key

        external_form_reference: None | str
        external_form_reference = self.external_form_reference

        custom_headers = self.custom_headers.to_dict()

        priority = self.priority

        tags = self.tags

        business_id: None | BusinessId
        business_id = self.business_id

        creation_date = self.creation_date.isoformat()

        variables = self.variables.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userTaskKey": user_task_key,
                "state": state,
                "elementId": element_id,
                "elementInstanceKey": element_instance_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "processDefinitionId": process_definition_id,
                "processDefinitionKey": process_definition_key,
                "processDefinitionVersion": process_definition_version,
                "tenantId": tenant_id,
                "assignee": assignee,
                "candidateGroups": candidate_groups,
                "candidateUsers": candidate_users,
                "dueDate": due_date,
                "followUpDate": follow_up_date,
                "formKey": form_key,
                "externalFormReference": external_form_reference,
                "customHeaders": custom_headers,
                "priority": priority,
                "tags": tags,
                "businessId": business_id,
                "creationDate": creation_date,
                "variables": variables,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_task_lookup_result_variables import (
            UserTaskLookupResultVariables,
        )
        from ..models.user_task_result_custom_headers import UserTaskResultCustomHeaders

        d = RequiredFields(src_dict, cls.__name__)
        user_task_key = UserTaskKey(d.pop_required("userTaskKey"))

        state = UserTaskLookupStateEnum(d.pop_required("state"))

        element_id = ElementId(d.pop_required("elementId"))

        element_instance_key = ElementInstanceKey(d.pop_required("elementInstanceKey"))

        process_instance_key = ProcessInstanceKey(d.pop_required("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop_required("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        process_definition_id = ProcessDefinitionId(
            d.pop_required("processDefinitionId")
        )

        process_definition_key = ProcessDefinitionKey(
            d.pop_required("processDefinitionKey")
        )

        process_definition_version = d.pop_required("processDefinitionVersion")

        tenant_id = TenantId(d.pop_required("tenantId"))

        def _parse_assignee(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        assignee = _parse_assignee(d.pop_required("assignee"))

        candidate_groups = cast(list[str], d.pop_required("candidateGroups"))

        candidate_users = cast(list[str], d.pop_required("candidateUsers"))

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

        due_date = _parse_due_date(d.pop_required("dueDate"))

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

        follow_up_date = _parse_follow_up_date(d.pop_required("followUpDate"))

        def _parse_form_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_form_key = _parse_form_key(d.pop_required("formKey"))

        form_key = (
            FormKey(_raw_form_key) if isinstance(_raw_form_key, str) else _raw_form_key
        )

        def _parse_external_form_reference(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_form_reference = _parse_external_form_reference(
            d.pop_required("externalFormReference")
        )

        custom_headers = UserTaskResultCustomHeaders.from_dict(
            d.pop_required("customHeaders")
        )

        priority = d.pop_required("priority")

        tags = cast(list[str], d.pop_required("tags"))

        def _parse_business_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_business_id = _parse_business_id(d.pop_required("businessId"))

        business_id = (
            BusinessId(_raw_business_id)
            if isinstance(_raw_business_id, str)
            else _raw_business_id
        )

        creation_date = isoparse(d.pop_required("creationDate"))

        variables = UserTaskLookupResultVariables.from_dict(d.pop_required("variables"))

        user_task_lookup_result = cls(
            user_task_key=user_task_key,
            state=state,
            element_id=element_id,
            element_instance_key=element_instance_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_definition_version=process_definition_version,
            tenant_id=tenant_id,
            assignee=assignee,
            candidate_groups=candidate_groups,
            candidate_users=candidate_users,
            due_date=due_date,
            follow_up_date=follow_up_date,
            form_key=form_key,
            external_form_reference=external_form_reference,
            custom_headers=custom_headers,
            priority=priority,
            tags=tags,
            business_id=business_id,
            creation_date=creation_date,
            variables=variables,
        )

        user_task_lookup_result.additional_properties = d
        return user_task_lookup_result

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
