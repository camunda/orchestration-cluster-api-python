from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_tenants_data import SearchTenantsData
from ...models.tenant_search_query_result import TenantSearchQueryResult
from ...types import UNSET, Response, Unset

def _get_kwargs(body: SearchTenantsData | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | TenantSearchQueryResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail | TenantSearchQueryResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: SearchTenantsData | Unset = UNSET
) -> Response[Any | ProblemDetail | TenantSearchQueryResult]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: SearchTenantsData | Unset = UNSET,
    **kwargs: Any,
) -> TenantSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: SearchTenantsData | Unset = UNSET
) -> Response[Any | ProblemDetail | TenantSearchQueryResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: SearchTenantsData | Unset = UNSET,
    **kwargs: Any,
) -> TenantSearchQueryResult: ...
