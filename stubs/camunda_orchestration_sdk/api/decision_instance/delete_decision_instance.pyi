from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.delete_process_instance_request_type_0 import (
    DeleteProcessInstanceRequestType0,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    decision_instance_key: str,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync_detailed(
    decision_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
def sync(
    decision_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
async def asyncio_detailed(
    decision_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]: ...
async def asyncio(
    decision_instance_key: str,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult: ...
