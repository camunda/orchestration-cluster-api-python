from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_group_search_result import RoleGroupSearchResult
from ...models.search_groups_for_role_data import SearchGroupsForRoleData
from ...types import UNSET, Response, Unset

def _get_kwargs(
    role_id: str, body: SearchGroupsForRoleData | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RoleGroupSearchResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RoleGroupSearchResult]: ...
def sync_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupsForRoleData | Unset = UNSET,
) -> Response[ProblemDetail | RoleGroupSearchResult]: ...
def sync(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupsForRoleData | Unset = UNSET,
    **kwargs: Any,
) -> RoleGroupSearchResult: ...
async def asyncio_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupsForRoleData | Unset = UNSET,
) -> Response[ProblemDetail | RoleGroupSearchResult]: ...
async def asyncio(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupsForRoleData | Unset = UNSET,
    **kwargs: Any,
) -> RoleGroupSearchResult: ...
