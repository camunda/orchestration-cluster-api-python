from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync_detailed(
    process_instance_key: str, client: AuthenticatedClient | Client
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync(
    process_instance_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationCreatedResult: ...
async def asyncio_detailed(
    process_instance_key: str, client: AuthenticatedClient | Client
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
async def asyncio(
    process_instance_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationCreatedResult: ...
