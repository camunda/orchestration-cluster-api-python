from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_mapping_rule_search_result import GroupMappingRuleSearchResult
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    group_id: str, *, body: MappingRuleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupMappingRuleSearchResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupMappingRuleSearchResult | ProblemDetail]: ...
def sync_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[GroupMappingRuleSearchResult | ProblemDetail]: ...
def sync(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupMappingRuleSearchResult: ...
async def asyncio_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[GroupMappingRuleSearchResult | ProblemDetail]: ...
async def asyncio(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupMappingRuleSearchResult: ...
