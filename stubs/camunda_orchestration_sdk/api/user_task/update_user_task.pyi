from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_task_update_request import UserTaskUpdateRequest
from ...types import UNSET, Response, Unset

def _get_kwargs(
    user_task_key: str, body: UserTaskUpdateRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: UserTaskUpdateRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail]: ...
def sync(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: UserTaskUpdateRequest | Unset = UNSET,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: UserTaskUpdateRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: UserTaskUpdateRequest | Unset = UNSET,
    **kwargs: Any,
) -> None: ...
