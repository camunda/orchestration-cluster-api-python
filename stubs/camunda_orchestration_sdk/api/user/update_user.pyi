from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_result import UserResult
from ...models.user_update_request import UserUpdateRequest
from ...types import Response

def _get_kwargs(username: str, body: UserUpdateRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UserResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | UserResult]: ...
def sync_detailed(
    username: str, client: AuthenticatedClient | Client, body: UserUpdateRequest
) -> Response[ProblemDetail | UserResult]: ...
def sync(
    username: str,
    client: AuthenticatedClient | Client,
    body: UserUpdateRequest,
    **kwargs: Any,
) -> UserResult: ...
async def asyncio_detailed(
    username: str, client: AuthenticatedClient | Client, body: UserUpdateRequest
) -> Response[ProblemDetail | UserResult]: ...
async def asyncio(
    username: str,
    client: AuthenticatedClient | Client,
    body: UserUpdateRequest,
    **kwargs: Any,
) -> UserResult: ...
