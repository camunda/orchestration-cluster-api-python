from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_update_request import GroupUpdateRequest
from ...models.group_update_result import GroupUpdateResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(group_id: str, body: GroupUpdateRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupUpdateResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupUpdateResult | ProblemDetail]: ...
def sync_detailed(
    group_id: str, client: AuthenticatedClient | Client, body: GroupUpdateRequest
) -> Response[GroupUpdateResult | ProblemDetail]: ...
def sync(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: GroupUpdateRequest,
    **kwargs: Any,
) -> GroupUpdateResult: ...
async def asyncio_detailed(
    group_id: str, client: AuthenticatedClient | Client, body: GroupUpdateRequest
) -> Response[GroupUpdateResult | ProblemDetail]: ...
async def asyncio(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: GroupUpdateRequest,
    **kwargs: Any,
) -> GroupUpdateResult: ...
