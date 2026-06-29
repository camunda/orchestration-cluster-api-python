from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.job_batch_update_request import JobBatchUpdateRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(*, body: JobBatchUpdateRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: JobBatchUpdateRequest
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, body: JobBatchUpdateRequest, **kwargs: Any
) -> BatchOperationCreatedResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: JobBatchUpdateRequest
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: JobBatchUpdateRequest, **kwargs: Any
) -> BatchOperationCreatedResult: ...
