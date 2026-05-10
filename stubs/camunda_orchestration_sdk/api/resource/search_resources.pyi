from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.resource_search_query import ResourceSearchQuery
from ...models.resource_search_query_result import ResourceSearchQueryResult
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: ResourceSearchQuery | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ResourceSearchQueryResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ResourceSearchQueryResult]: ...
def sync_detailed(
    *, client: AuthenticatedClient | Client, body: ResourceSearchQuery | Unset = UNSET
) -> Response[ProblemDetail | ResourceSearchQueryResult]: ...
def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ResourceSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> ResourceSearchQueryResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: ResourceSearchQuery | Unset = UNSET
) -> Response[ProblemDetail | ResourceSearchQueryResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ResourceSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> ResourceSearchQueryResult: ...
