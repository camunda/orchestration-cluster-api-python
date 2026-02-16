from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.job_update_request import JobUpdateRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(job_key: str, body: JobUpdateRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    job_key: str, client: AuthenticatedClient | Client, body: JobUpdateRequest
) -> Response[Any | ProblemDetail]: ...
def sync(
    job_key: str,
    client: AuthenticatedClient | Client,
    body: JobUpdateRequest,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    job_key: str, client: AuthenticatedClient | Client, body: JobUpdateRequest
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    job_key: str,
    client: AuthenticatedClient | Client,
    body: JobUpdateRequest,
    **kwargs: Any,
) -> None: ...
