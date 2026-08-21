from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.exporting_status_response import ExportingStatusResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ExportingStatusResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ExportingStatusResponse | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ExportingStatusResponse | ProblemDetail]: ...
def sync(*, client: AuthenticatedClient, **kwargs: Any) -> ExportingStatusResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ExportingStatusResponse | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> ExportingStatusResponse: ...
