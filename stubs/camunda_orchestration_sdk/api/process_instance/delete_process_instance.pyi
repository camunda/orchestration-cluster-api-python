from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.delete_process_instance_data_type_0 import DeleteProcessInstanceDataType0
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    process_instance_key: str,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync_detailed(
    process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync(
    process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
async def asyncio_detailed(
    process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
async def asyncio(
    process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
