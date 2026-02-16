from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.mapping_rule_search_query_result import MappingRuleSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> MappingRuleSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MappingRuleSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[MappingRuleSearchQueryResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[MappingRuleSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleSearchQueryResult: ...
