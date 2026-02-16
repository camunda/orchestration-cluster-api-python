from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_users_for_group_data import SearchUsersForGroupData
from ...models.tenant_user_search_result import TenantUserSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    group_id: str, body: SearchUsersForGroupData | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantUserSearchResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
def sync_detailed(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForGroupData | Unset = UNSET,
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
def sync(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForGroupData | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
async def asyncio_detailed(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForGroupData | Unset = UNSET,
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
async def asyncio(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForGroupData | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
