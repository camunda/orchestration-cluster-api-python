from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.tenant_mapping_rule_search_result import TenantMappingRuleSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    tenant_id: str, *, body: MappingRuleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> TenantMappingRuleSearchResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[TenantMappingRuleSearchResult]: ...
def sync_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[TenantMappingRuleSearchResult]: ...
def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> TenantMappingRuleSearchResult: ...
async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[TenantMappingRuleSearchResult]: ...
async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> TenantMappingRuleSearchResult: ...
