from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_role_search_result import GroupRoleSearchResult
from ...models.problem_detail import ProblemDetail
from ...models.role_search_query_request import RoleSearchQueryRequest
from ...types import UNSET, Response, Unset

def _get_kwargs(
    group_id: str, *, body: RoleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupRoleSearchResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupRoleSearchResult | ProblemDetail]: ...
def sync_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[GroupRoleSearchResult | ProblemDetail]: ...
def sync(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupRoleSearchResult: ...
async def asyncio_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[GroupRoleSearchResult | ProblemDetail]: ...
async def asyncio(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupRoleSearchResult: ...
