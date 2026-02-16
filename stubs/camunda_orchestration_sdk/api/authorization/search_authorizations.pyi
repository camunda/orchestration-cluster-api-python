from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.authorization_search_query import AuthorizationSearchQuery
from ...models.authorization_search_result import AuthorizationSearchResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(body: AuthorizationSearchQuery | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> AuthorizationSearchResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuthorizationSearchResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[AuthorizationSearchResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AuthorizationSearchResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[AuthorizationSearchResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AuthorizationSearchResult: ...
