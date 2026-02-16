from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_update_request import RoleUpdateRequest
from ...models.role_update_result import RoleUpdateResult
from ...types import Response

def _get_kwargs(role_id: str, body: RoleUpdateRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RoleUpdateResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RoleUpdateResult]: ...
def sync_detailed(
    role_id: str, client: AuthenticatedClient | Client, body: RoleUpdateRequest
) -> Response[ProblemDetail | RoleUpdateResult]: ...
def sync(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: RoleUpdateRequest,
    **kwargs: Any,
) -> RoleUpdateResult: ...
async def asyncio_detailed(
    role_id: str, client: AuthenticatedClient | Client, body: RoleUpdateRequest
) -> Response[ProblemDetail | RoleUpdateResult]: ...
async def asyncio(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: RoleUpdateRequest,
    **kwargs: Any,
) -> RoleUpdateResult: ...
