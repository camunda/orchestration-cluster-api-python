from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_search_query_request import UserSearchQueryRequest
from ...models.user_search_result import UserSearchResult
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: UserSearchQueryRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UserSearchResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | UserSearchResult]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: UserSearchQueryRequest | Unset = UNSET
) -> Response[ProblemDetail | UserSearchResult]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: UserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserSearchResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: UserSearchQueryRequest | Unset = UNSET
) -> Response[ProblemDetail | UserSearchResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: UserSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserSearchResult: ...
