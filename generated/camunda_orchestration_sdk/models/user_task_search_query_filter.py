from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    UserTaskKey,
    lift_element_id,
    lift_element_instance_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_user_task_key,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_task_state_exact_match import UserTaskStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.advanced_user_task_state_filter import AdvancedUserTaskStateFilter
    from ..models.variable_value_filter_property import VariableValueFilterProperty


T = TypeVar("T", bound="UserTaskSearchQueryFilter")


@_attrs_define
class UserTaskSearchQueryFilter:
    """The user task search filters.

    Attributes:
        state (AdvancedUserTaskStateFilter | Unset | UserTaskStateExactMatch):
        assignee (AdvancedStringFilter | str | Unset):
        priority (AdvancedIntegerFilter | int | Unset):
        element_id (str | Unset): The element ID of the user task. Example: Activity_106kosb.
        name (AdvancedStringFilter | str | Unset):
        candidate_group (AdvancedStringFilter | str | Unset):
        candidate_user (AdvancedStringFilter | str | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
        process_definition_id (str | Unset): The ID of the process definition. Example: new-account-onboarding-workflow.
        creation_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        completion_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        follow_up_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        due_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        process_instance_variables (list[VariableValueFilterProperty] | Unset):
        local_variables (list[VariableValueFilterProperty] | Unset):
        user_task_key (str | Unset): The key for this user task.
        process_definition_key (str | Unset): The key of the process definition. Example: 2251799813686749.
        process_instance_key (str | Unset): The key of the process instance. Example: 2251799813690746.
        element_instance_key (str | Unset): The key of the element instance. Example: 2251799813686789.
        tags (list[str] | Unset): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or
            `.`; length ≤ 100. Example: ['high-touch', 'remediation'].
    """

    state: AdvancedUserTaskStateFilter | Unset | UserTaskStateExactMatch = UNSET
    assignee: AdvancedStringFilter | str | Unset = UNSET
    priority: AdvancedIntegerFilter | int | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    candidate_group: AdvancedStringFilter | str | Unset = UNSET
    candidate_user: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    creation_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    completion_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    follow_up_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    due_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    process_instance_variables: list[VariableValueFilterProperty] | Unset = UNSET
    local_variables: list[VariableValueFilterProperty] | Unset = UNSET
    user_task_key: UserTaskKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        state: dict[str, Any] | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, UserTaskStateExactMatch):
            state = self.state.value
        else:
            state = self.state.to_dict()

        assignee: dict[str, Any] | str | Unset
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        elif isinstance(self.assignee, AdvancedStringFilter):
            assignee = self.assignee.to_dict()
        else:
            assignee = self.assignee

        priority: dict[str, Any] | int | Unset
        if isinstance(self.priority, Unset):
            priority = UNSET
        elif isinstance(self.priority, AdvancedIntegerFilter):
            priority = self.priority.to_dict()
        else:
            priority = self.priority

        element_id = self.element_id

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        candidate_group: dict[str, Any] | str | Unset
        if isinstance(self.candidate_group, Unset):
            candidate_group = UNSET
        elif isinstance(self.candidate_group, AdvancedStringFilter):
            candidate_group = self.candidate_group.to_dict()
        else:
            candidate_group = self.candidate_group

        candidate_user: dict[str, Any] | str | Unset
        if isinstance(self.candidate_user, Unset):
            candidate_user = UNSET
        elif isinstance(self.candidate_user, AdvancedStringFilter):
            candidate_user = self.candidate_user.to_dict()
        else:
            candidate_user = self.candidate_user

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        process_definition_id = self.process_definition_id

        creation_date: dict[str, Any] | str | Unset
        if isinstance(self.creation_date, Unset):
            creation_date = UNSET
        elif isinstance(self.creation_date, datetime.datetime):
            creation_date = self.creation_date.isoformat()
        else:
            creation_date = self.creation_date.to_dict()

        completion_date: dict[str, Any] | str | Unset
        if isinstance(self.completion_date, Unset):
            completion_date = UNSET
        elif isinstance(self.completion_date, datetime.datetime):
            completion_date = self.completion_date.isoformat()
        else:
            completion_date = self.completion_date.to_dict()

        follow_up_date: dict[str, Any] | str | Unset
        if isinstance(self.follow_up_date, Unset):
            follow_up_date = UNSET
        elif isinstance(self.follow_up_date, datetime.datetime):
            follow_up_date = self.follow_up_date.isoformat()
        else:
            follow_up_date = self.follow_up_date.to_dict()

        due_date: dict[str, Any] | str | Unset
        if isinstance(self.due_date, Unset):
            due_date = UNSET
        elif isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date.to_dict()

        process_instance_variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.process_instance_variables, Unset):
            process_instance_variables = []
            for process_instance_variables_item_data in self.process_instance_variables:
                process_instance_variables_item = (
                    process_instance_variables_item_data.to_dict()
                )
                process_instance_variables.append(process_instance_variables_item)

        local_variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.local_variables, Unset):
            local_variables = []
            for local_variables_item_data in self.local_variables:
                local_variables_item = local_variables_item_data.to_dict()
                local_variables.append(local_variables_item)

        user_task_key = self.user_task_key

        process_definition_key = self.process_definition_key

        process_instance_key = self.process_instance_key

        element_instance_key = self.element_instance_key

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if priority is not UNSET:
            field_dict["priority"] = priority
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if name is not UNSET:
            field_dict["name"] = name
        if candidate_group is not UNSET:
            field_dict["candidateGroup"] = candidate_group
        if candidate_user is not UNSET:
            field_dict["candidateUser"] = candidate_user
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if completion_date is not UNSET:
            field_dict["completionDate"] = completion_date
        if follow_up_date is not UNSET:
            field_dict["followUpDate"] = follow_up_date
        if due_date is not UNSET:
            field_dict["dueDate"] = due_date
        if process_instance_variables is not UNSET:
            field_dict["processInstanceVariables"] = process_instance_variables
        if local_variables is not UNSET:
            field_dict["localVariables"] = local_variables
        if user_task_key is not UNSET:
            field_dict["userTaskKey"] = user_task_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.advanced_user_task_state_filter import AdvancedUserTaskStateFilter
        from ..models.variable_value_filter_property import VariableValueFilterProperty

        d = dict(src_dict)

        def _parse_state(
            data: object,
        ) -> AdvancedUserTaskStateFilter | Unset | UserTaskStateExactMatch:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = UserTaskStateExactMatch(data)

                return state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            state_type_1 = AdvancedUserTaskStateFilter.from_dict(data)

            return state_type_1

        state = _parse_state(d.pop("state", UNSET))

        def _parse_assignee(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                assignee_type_1 = AdvancedStringFilter.from_dict(data)

                return assignee_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        assignee = _parse_assignee(d.pop("assignee", UNSET))

        def _parse_priority(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                priority_type_1 = AdvancedIntegerFilter.from_dict(data)

                return priority_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        priority = _parse_priority(d.pop("priority", UNSET))

        element_id = (
            lift_element_id(_val)
            if (_val := d.pop("elementId", UNSET)) is not UNSET
            else UNSET
        )

        def _parse_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = AdvancedStringFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_candidate_group(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                candidate_group_type_1 = AdvancedStringFilter.from_dict(data)

                return candidate_group_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        candidate_group = _parse_candidate_group(d.pop("candidateGroup", UNSET))

        def _parse_candidate_user(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                candidate_user_type_1 = AdvancedStringFilter.from_dict(data)

                return candidate_user_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        candidate_user = _parse_candidate_user(d.pop("candidateUser", UNSET))

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

        process_definition_id = (
            lift_process_definition_id(_val)
            if (_val := d.pop("processDefinitionId", UNSET)) is not UNSET
            else UNSET
        )

        def _parse_creation_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                creation_date_type_0 = isoparse(data)

                return creation_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            creation_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return creation_date_type_1

        creation_date = _parse_creation_date(d.pop("creationDate", UNSET))

        def _parse_completion_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completion_date_type_0 = isoparse(data)

                return completion_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            completion_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return completion_date_type_1

        completion_date = _parse_completion_date(d.pop("completionDate", UNSET))

        def _parse_follow_up_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                follow_up_date_type_0 = isoparse(data)

                return follow_up_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            follow_up_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return follow_up_date_type_1

        follow_up_date = _parse_follow_up_date(d.pop("followUpDate", UNSET))

        def _parse_due_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data)

                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            due_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return due_date_type_1

        due_date = _parse_due_date(d.pop("dueDate", UNSET))

        _process_instance_variables = d.pop("processInstanceVariables", UNSET)
        process_instance_variables: list[VariableValueFilterProperty] | Unset = UNSET
        if _process_instance_variables is not UNSET:
            process_instance_variables = []
            for process_instance_variables_item_data in _process_instance_variables:
                process_instance_variables_item = VariableValueFilterProperty.from_dict(
                    process_instance_variables_item_data
                )

                process_instance_variables.append(process_instance_variables_item)

        _local_variables = d.pop("localVariables", UNSET)
        local_variables: list[VariableValueFilterProperty] | Unset = UNSET
        if _local_variables is not UNSET:
            local_variables = []
            for local_variables_item_data in _local_variables:
                local_variables_item = VariableValueFilterProperty.from_dict(
                    local_variables_item_data
                )

                local_variables.append(local_variables_item)

        user_task_key = (
            lift_user_task_key(_val)
            if (_val := d.pop("userTaskKey", UNSET)) is not UNSET
            else UNSET
        )

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

        element_instance_key = (
            lift_element_instance_key(_val)
            if (_val := d.pop("elementInstanceKey", UNSET)) is not UNSET
            else UNSET
        )

        tags = cast(list[str], d.pop("tags", UNSET))

        user_task_search_query_filter = cls(
            state=state,
            assignee=assignee,
            priority=priority,
            element_id=element_id,
            name=name,
            candidate_group=candidate_group,
            candidate_user=candidate_user,
            tenant_id=tenant_id,
            process_definition_id=process_definition_id,
            creation_date=creation_date,
            completion_date=completion_date,
            follow_up_date=follow_up_date,
            due_date=due_date,
            process_instance_variables=process_instance_variables,
            local_variables=local_variables,
            user_task_key=user_task_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            tags=tags,
        )

        user_task_search_query_filter.additional_properties = d
        return user_task_search_query_filter

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
