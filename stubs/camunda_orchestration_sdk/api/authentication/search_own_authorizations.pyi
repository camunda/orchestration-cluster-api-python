from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.authorization_search_query import AuthorizationSearchQuery
from ...models.own_authorization_search_result import OwnAuthorizationSearchResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: AuthorizationSearchQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OwnAuthorizationSearchResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> OwnAuthorizationSearchResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> OwnAuthorizationSearchResult: ...
