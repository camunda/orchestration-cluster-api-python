from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.problem_detail import ProblemDetail
from ...models.search_query_response import SearchQueryResponse
from ...types import UNSET, Response, Unset

def _get_kwargs(
    role_id: str, body: MappingRuleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SearchQueryResponse | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SearchQueryResponse]: ...
def sync_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]: ...
def sync(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
async def asyncio_detailed(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]: ...
async def asyncio(
    role_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
