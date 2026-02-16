from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.search_group_ids_for_tenant_data import SearchGroupIdsForTenantData
from ...models.tenant_group_search_result import TenantGroupSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    tenant_id: str, body: SearchGroupIdsForTenantData | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> TenantGroupSearchResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[TenantGroupSearchResult]: ...
def sync_detailed(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupIdsForTenantData | Unset = UNSET,
) -> Response[TenantGroupSearchResult]: ...
def sync(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupIdsForTenantData | Unset = UNSET,
    **kwargs: Any,
) -> TenantGroupSearchResult: ...
async def asyncio_detailed(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupIdsForTenantData | Unset = UNSET,
) -> Response[TenantGroupSearchResult]: ...
async def asyncio(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: SearchGroupIdsForTenantData | Unset = UNSET,
    **kwargs: Any,
) -> TenantGroupSearchResult: ...
