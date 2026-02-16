from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(user_task_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    user_task_key: str, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]: ...
def sync(
    user_task_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> None: ...
async def asyncio_detailed(
    user_task_key: str, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    user_task_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> None: ...
