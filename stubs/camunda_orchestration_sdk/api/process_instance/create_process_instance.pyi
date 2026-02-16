from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.create_process_instance_result import CreateProcessInstanceResult
from ...models.problem_detail import ProblemDetail
from ...models.process_creation_by_id import ProcessCreationById
from ...models.process_creation_by_key import ProcessCreationByKey
from ...types import Response

def _get_kwargs(body: ProcessCreationById | ProcessCreationByKey) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateProcessInstanceResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
    **kwargs: Any,
) -> CreateProcessInstanceResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
    **kwargs: Any,
) -> CreateProcessInstanceResult: ...
