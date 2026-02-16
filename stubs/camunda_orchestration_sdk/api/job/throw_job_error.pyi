from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.job_error_request import JobErrorRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(job_key: str, body: JobErrorRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    job_key: str, client: AuthenticatedClient | Client, body: JobErrorRequest
) -> Response[Any | ProblemDetail]: ...
def sync(
    job_key: str,
    client: AuthenticatedClient | Client,
    body: JobErrorRequest,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    job_key: str, client: AuthenticatedClient | Client, body: JobErrorRequest
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    job_key: str,
    client: AuthenticatedClient | Client,
    body: JobErrorRequest,
    **kwargs: Any,
) -> None: ...
