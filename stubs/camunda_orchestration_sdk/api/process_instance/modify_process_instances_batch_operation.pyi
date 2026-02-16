from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.modify_process_instances_batch_operation_data import (
    ModifyProcessInstancesBatchOperationData,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(body: ModifyProcessInstancesBatchOperationData) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: ModifyProcessInstancesBatchOperationData
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: ModifyProcessInstancesBatchOperationData,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: ModifyProcessInstancesBatchOperationData
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: ModifyProcessInstancesBatchOperationData,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
