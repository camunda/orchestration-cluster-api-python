from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_response import BatchOperationResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(batch_operation_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationResponse | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationResponse | ProblemDetail]: ...
def sync_detailed(
    batch_operation_key: str, client: AuthenticatedClient | Client
) -> Response[BatchOperationResponse | ProblemDetail]: ...
def sync(
    batch_operation_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationResponse: ...
async def asyncio_detailed(
    batch_operation_key: str, client: AuthenticatedClient | Client
) -> Response[BatchOperationResponse | ProblemDetail]: ...
async def asyncio(
    batch_operation_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationResponse: ...
