from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_user_tasks_data import SearchUserTasksData
from ...models.search_user_tasks_response_200 import SearchUserTasksResponse200
from ...types import UNSET, Response, Unset

def _get_kwargs(body: SearchUserTasksData | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SearchUserTasksResponse200 | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SearchUserTasksResponse200]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: SearchUserTasksData | Unset = UNSET
) -> Response[ProblemDetail | SearchUserTasksResponse200]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: SearchUserTasksData | Unset = UNSET,
    **kwargs: Any,
) -> SearchUserTasksResponse200: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: SearchUserTasksData | Unset = UNSET
) -> Response[ProblemDetail | SearchUserTasksResponse200]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: SearchUserTasksData | Unset = UNSET,
    **kwargs: Any,
) -> SearchUserTasksResponse200: ...
