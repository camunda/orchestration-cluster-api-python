from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_users_for_role_data import SearchUsersForRoleData
from ...models.tenant_user_search_result import TenantUserSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    role_id: str, body: SearchUsersForRoleData | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantUserSearchResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
def sync_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForRoleData | Unset = UNSET,
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
def sync(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForRoleData | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
async def asyncio_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForRoleData | Unset = UNSET,
) -> Response[ProblemDetail | TenantUserSearchResult]: ...
async def asyncio(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchUsersForRoleData | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
