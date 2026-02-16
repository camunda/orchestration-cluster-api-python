from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_create_request import RoleCreateRequest
from ...models.role_create_result import RoleCreateResult
from ...types import UNSET, Response, Unset

def _get_kwargs(body: RoleCreateRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RoleCreateResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RoleCreateResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: RoleCreateRequest | Unset = UNSET
) -> Response[ProblemDetail | RoleCreateResult]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: RoleCreateRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleCreateResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: RoleCreateRequest | Unset = UNSET
) -> Response[ProblemDetail | RoleCreateResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: RoleCreateRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleCreateResult: ...
