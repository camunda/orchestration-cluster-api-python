# Compilable usage examples for user task operations.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

import datetime

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.changeset_type_0 import ChangesetType0
from camunda_orchestration_sdk.semantic_types import UserTaskKey
from camunda_orchestration_sdk.models.search_user_tasks_data import (
    SearchUserTasksData,
)
from camunda_orchestration_sdk.models.user_task_assignment_request import (
    UserTaskAssignmentRequest,
)
from camunda_orchestration_sdk.models.user_task_completion_request import (
    UserTaskCompletionRequest,
)
from camunda_orchestration_sdk.models.user_task_completion_request_variables import (
    UserTaskCompletionRequestVariables,
)
from camunda_orchestration_sdk.models.user_task_update_request import (
    UserTaskUpdateRequest,
)
from camunda_orchestration_sdk.types import Unset


# region SearchUserTasks
def search_user_tasks_example() -> None:
    client = CamundaClient()

    result = client.search_user_tasks(
        data=SearchUserTasksData()
    )

    if not isinstance(result.items, Unset):
        for task in result.items:
            print(f"Task: {task.user_task_key}")
# endregion SearchUserTasks


# region AssignUserTask
def assign_user_task_example() -> None:
    client = CamundaClient()

    client.assign_user_task(
        user_task_key=UserTaskKey("123456"),
        data=UserTaskAssignmentRequest(
            assignee="user@example.com",
        ),
    )
# endregion AssignUserTask


# region UnassignUserTask
def unassign_user_task_example() -> None:
    client = CamundaClient()

    client.unassign_user_task(user_task_key=UserTaskKey("123456"))
# endregion UnassignUserTask


# region CompleteUserTask
def complete_user_task_example() -> None:
    client = CamundaClient()

    variables = UserTaskCompletionRequestVariables()
    variables["approved"] = True

    client.complete_user_task(
        user_task_key=UserTaskKey("123456"),
        data=UserTaskCompletionRequest(
            variables=variables,
        ),
    )
# endregion CompleteUserTask


# region UpdateUserTask
def update_user_task_example() -> None:
    client = CamundaClient()

    client.update_user_task(
        user_task_key=UserTaskKey("123456"),
        data=UserTaskUpdateRequest(
            changeset=ChangesetType0(
                due_date=datetime.datetime(2025, 12, 31, 23, 59, 59),
            ),
        ),
    )
# endregion UpdateUserTask


# region GetUserTask
def get_user_task_example() -> None:
    client = CamundaClient()

    task = client.get_user_task(user_task_key=UserTaskKey("123456"))

    print(f"Task: {task.user_task_key}")
# endregion GetUserTask
