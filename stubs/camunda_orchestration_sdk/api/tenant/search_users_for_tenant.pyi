from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.tenant_user_search_query_request import TenantUserSearchQueryRequest
from ...models.tenant_user_search_result import TenantUserSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    tenant_id: str, *, body: TenantUserSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> TenantUserSearchResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[TenantUserSearchResult]: ...
def sync_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient,
    body: TenantUserSearchQueryRequest | Unset = UNSET,
) -> Response[TenantUserSearchResult]: ...
def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient,
    body: TenantUserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient,
    body: TenantUserSearchQueryRequest | Unset = UNSET,
) -> Response[TenantUserSearchResult]: ...
async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient,
    body: TenantUserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> TenantUserSearchResult: ...
