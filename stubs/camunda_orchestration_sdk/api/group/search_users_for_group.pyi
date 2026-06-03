from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.group_user_search_query_request import GroupUserSearchQueryRequest
from ...models.group_user_search_result import GroupUserSearchResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    group_id: str, *, body: GroupUserSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupUserSearchResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupUserSearchResult | ProblemDetail]: ...
def sync_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: GroupUserSearchQueryRequest | Unset = UNSET,
) -> Response[GroupUserSearchResult | ProblemDetail]: ...
def sync(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: GroupUserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupUserSearchResult: ...
async def asyncio_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: GroupUserSearchQueryRequest | Unset = UNSET,
) -> Response[GroupUserSearchResult | ProblemDetail]: ...
async def asyncio(
    group_id: str,
    *,
    client: AuthenticatedClient,
    body: GroupUserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> GroupUserSearchResult: ...
