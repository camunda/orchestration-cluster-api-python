from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.secret_resolve_request import SecretResolveRequest
from ...models.secret_resolve_result import SecretResolveResult
from ...types import Response

def _get_kwargs(*, body: SecretResolveRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SecretResolveResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SecretResolveResult]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: SecretResolveRequest
) -> Response[ProblemDetail | SecretResolveResult]: ...
def sync(
    *, client: AuthenticatedClient, body: SecretResolveRequest, **kwargs: Any
) -> SecretResolveResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: SecretResolveRequest
) -> Response[ProblemDetail | SecretResolveResult]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: SecretResolveRequest, **kwargs: Any
) -> SecretResolveResult: ...
