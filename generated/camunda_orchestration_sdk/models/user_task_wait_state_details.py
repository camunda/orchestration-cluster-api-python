from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import UserTaskKey

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserTaskWaitStateDetails")


@_attrs_define
class UserTaskWaitStateDetails:
    """
    Attributes:
        task_key (str): The key of the user task.
        due_date (datetime.datetime | None): The due date of the user task, if set.
        wait_state_type (str): The wait state type discriminator.
    """

    task_key: UserTaskKey
    due_date: datetime.datetime | None
    wait_state_type: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        task_key = self.task_key

        due_date: None | str
        if isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        wait_state_type = self.wait_state_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "taskKey": task_key,
                "dueDate": due_date,
                "waitStateType": wait_state_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        task_key = UserTaskKey(d.pop("taskKey"))

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

        wait_state_type = d.pop("waitStateType")

        user_task_wait_state_details = cls(
            task_key=task_key,
            due_date=due_date,
            wait_state_type=wait_state_type,
        )

        user_task_wait_state_details.additional_properties = d
        return user_task_wait_state_details

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
