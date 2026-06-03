from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_client_search_query_request import RoleClientSearchQueryRequest
from ...models.role_client_search_result import RoleClientSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    role_id: str, *, body: RoleClientSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RoleClientSearchResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RoleClientSearchResult]: ...
def sync_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleClientSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | RoleClientSearchResult]: ...
def sync(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleClientSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleClientSearchResult: ...
async def asyncio_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleClientSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | RoleClientSearchResult]: ...
async def asyncio(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleClientSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> RoleClientSearchResult: ...
