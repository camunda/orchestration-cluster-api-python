from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.license_response import LicenseResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> LicenseResponse | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[LicenseResponse | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
) -> Response[LicenseResponse | ProblemDetail]: ...
def sync(client: AuthenticatedClient | Client, **kwargs: Any) -> LicenseResponse: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
) -> Response[LicenseResponse | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client, **kwargs: Any
) -> LicenseResponse: ...
