from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.resource_result import ResourceResult
from ...types import Response

def _get_kwargs(resource_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ResourceResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ResourceResult]: ...
def sync_detailed(
    resource_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ResourceResult]: ...
def sync(
    resource_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ResourceResult: ...
async def asyncio_detailed(
    resource_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ResourceResult]: ...
async def asyncio(
    resource_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ResourceResult: ...
