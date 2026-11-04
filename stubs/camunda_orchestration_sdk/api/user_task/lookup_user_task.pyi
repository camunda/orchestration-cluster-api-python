from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_task_lookup_request import UserTaskLookupRequest
from ...models.user_task_lookup_result import UserTaskLookupResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    user_task_key: str, *, body: UserTaskLookupRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UserTaskLookupResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | UserTaskLookupResult]: ...
def sync_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
) -> Response[ProblemDetail | UserTaskLookupResult]: ...
def sync(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserTaskLookupResult: ...
async def asyncio_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
) -> Response[ProblemDetail | UserTaskLookupResult]: ...
async def asyncio(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserTaskLookupResult: ...
