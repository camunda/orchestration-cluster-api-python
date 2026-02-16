from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_result import GroupResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(group_id: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupResult | ProblemDetail]: ...
def sync_detailed(
    group_id: str, client: AuthenticatedClient | Client
) -> Response[GroupResult | ProblemDetail]: ...
def sync(
    group_id: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GroupResult: ...
async def asyncio_detailed(
    group_id: str, client: AuthenticatedClient | Client
) -> Response[GroupResult | ProblemDetail]: ...
async def asyncio(
    group_id: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GroupResult: ...
