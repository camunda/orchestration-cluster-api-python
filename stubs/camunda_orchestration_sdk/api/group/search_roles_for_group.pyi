from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.role_search_query_request import RoleSearchQueryRequest
from ...models.search_query_response import SearchQueryResponse
from ...types import UNSET, Response, Unset

def _get_kwargs(
    group_id: str, body: RoleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SearchQueryResponse | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SearchQueryResponse]: ...
def sync_detailed(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]: ...
def sync(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
async def asyncio_detailed(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]: ...
async def asyncio(
    group_id: str,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse: ...
