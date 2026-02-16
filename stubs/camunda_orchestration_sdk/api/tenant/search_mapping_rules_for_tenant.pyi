from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.search_query_response import SearchQueryResponse
from ...types import UNSET, Response, Unset

def _get_kwargs(
    tenant_id: str, body: MappingRuleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> SearchQueryResponse | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SearchQueryResponse]: ...
def sync_detailed(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[SearchQueryResponse]: ...
def sync(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
async def asyncio_detailed(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[SearchQueryResponse]: ...
async def asyncio(
    tenant_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
