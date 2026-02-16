from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_search_query_request import GroupSearchQueryRequest
from ...models.group_search_query_result import GroupSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(body: GroupSearchQueryRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GroupSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | GroupSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: GroupSearchQueryRequest | Unset = UNSET
) -> Response[Any | GroupSearchQueryResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: GroupSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: GroupSearchQueryRequest | Unset = UNSET
) -> Response[Any | GroupSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: GroupSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupSearchQueryResult: ...
