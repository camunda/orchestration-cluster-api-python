from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    FormKey,
    UserTaskKey,
    lift_form_key,
    lift_user_task_key,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ActivatedJobResultUserTask")


@_attrs_define
class ActivatedJobResultUserTask:
    """User task properties, if the job is a user task.
    This is `null` if the job is not a user task.

        Attributes:
            action (str): The action performed on the user task.
            assignee (None | str): The user assigned to the task.
            candidate_groups (list[str]): The groups eligible to claim the task.
            candidate_users (list[str]): The users eligible to claim the task.
            changed_attributes (list[str]): The attributes that were changed in the task.
            due_date (None | str): The due date of the user task in ISO 8601 format.
            follow_up_date (None | str): The follow-up date of the user task in ISO 8601 format.
            form_key (None | str): The key of the form associated with the user task. Example: 2251799813684365.
            priority (int | None): The priority of the user task.
            user_task_key (None | str): The unique key identifying the user task.
    """

    action: str
    assignee: None | str
    candidate_groups: list[str]
    candidate_users: list[str]
    changed_attributes: list[str]
    due_date: None | str
    follow_up_date: None | str
    form_key: None | FormKey
    priority: int | None
    user_task_key: None | UserTaskKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        assignee: None | str
        assignee = self.assignee

        candidate_groups = self.candidate_groups

        candidate_users = self.candidate_users

        changed_attributes = self.changed_attributes

        due_date: None | str
        due_date = self.due_date

        follow_up_date: None | str
        follow_up_date = self.follow_up_date

        form_key: None | FormKey
        form_key = self.form_key

        priority: int | None
        priority = self.priority

        user_task_key: None | UserTaskKey
        user_task_key = self.user_task_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "assignee": assignee,
                "candidateGroups": candidate_groups,
                "candidateUsers": candidate_users,
                "changedAttributes": changed_attributes,
                "dueDate": due_date,
                "followUpDate": follow_up_date,
                "formKey": form_key,
                "priority": priority,
                "userTaskKey": user_task_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = d.pop("action")

        def _parse_assignee(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        assignee = _parse_assignee(d.pop("assignee"))

        candidate_groups = cast(list[str], d.pop("candidateGroups"))

        candidate_users = cast(list[str], d.pop("candidateUsers"))

        changed_attributes = cast(list[str], d.pop("changedAttributes"))

        def _parse_due_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        due_date = _parse_due_date(d.pop("dueDate"))

        def _parse_follow_up_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        follow_up_date = _parse_follow_up_date(d.pop("followUpDate"))

        def _parse_form_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_form_key = _parse_form_key(d.pop("formKey"))

        form_key = lift_form_key(_raw_form_key)

        def _parse_priority(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        priority = _parse_priority(d.pop("priority"))

        def _parse_user_task_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_user_task_key = _parse_user_task_key(d.pop("userTaskKey"))

        user_task_key = lift_user_task_key(_raw_user_task_key)

        activated_job_result_user_task = cls(
            action=action,
            assignee=assignee,
            candidate_groups=candidate_groups,
            candidate_users=candidate_users,
            changed_attributes=changed_attributes,
            due_date=due_date,
            follow_up_date=follow_up_date,
            form_key=form_key,
            priority=priority,
            user_task_key=user_task_key,
        )

        activated_job_result_user_task.additional_properties = d
        return activated_job_result_user_task

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
