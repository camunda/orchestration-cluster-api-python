from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.get_user_task_response_200 import GetUserTaskResponse200
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(user_task_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> GetUserTaskResponse200 | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetUserTaskResponse200 | ProblemDetail]: ...
def sync_detailed(
    user_task_key: str, client: AuthenticatedClient | Client
) -> Response[GetUserTaskResponse200 | ProblemDetail]: ...
def sync(
    user_task_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetUserTaskResponse200: ...
async def asyncio_detailed(
    user_task_key: str, client: AuthenticatedClient | Client
) -> Response[GetUserTaskResponse200 | ProblemDetail]: ...
async def asyncio(
    user_task_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetUserTaskResponse200: ...
