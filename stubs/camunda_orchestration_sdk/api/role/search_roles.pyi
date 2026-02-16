from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_search_query_request import RoleSearchQueryRequest
from ...models.role_search_query_result import RoleSearchQueryResult
from ...types import UNSET, Response, Unset

def _get_kwargs(body: RoleSearchQueryRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | RoleSearchQueryResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail | RoleSearchQueryResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: RoleSearchQueryRequest | Unset = UNSET
) -> Response[Any | ProblemDetail | RoleSearchQueryResult]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: RoleSearchQueryRequest | Unset = UNSET
) -> Response[Any | ProblemDetail | RoleSearchQueryResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleSearchQueryResult: ...
