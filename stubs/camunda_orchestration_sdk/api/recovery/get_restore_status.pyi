from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.restore_status_response import RestoreStatusResponse
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | RestoreStatusResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail | RestoreStatusResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[Any | ProblemDetail | RestoreStatusResponse]: ...
def sync(*, client: AuthenticatedClient, **kwargs: Any) -> RestoreStatusResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[Any | ProblemDetail | RestoreStatusResponse]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RestoreStatusResponse: ...
