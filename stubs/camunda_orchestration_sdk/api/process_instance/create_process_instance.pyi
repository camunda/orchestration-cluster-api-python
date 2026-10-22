from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.create_process_instance_result import CreateProcessInstanceResult
from ...models.problem_detail import ProblemDetail
from ...models.process_creation_by_id import ProcessCreationById
from ...models.process_creation_by_key import ProcessCreationByKey
from ...models.process_creation_by_version_tag import ProcessCreationByVersionTag
from ...types import Response

def _get_kwargs(
    *, body: ProcessCreationById | ProcessCreationByKey | ProcessCreationByVersionTag
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateProcessInstanceResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessCreationById | ProcessCreationByKey | ProcessCreationByVersionTag,
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: ProcessCreationById | ProcessCreationByKey | ProcessCreationByVersionTag,
    **kwargs: Any,
) -> CreateProcessInstanceResult: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessCreationById | ProcessCreationByKey | ProcessCreationByVersionTag,
) -> Response[CreateProcessInstanceResult | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProcessCreationById | ProcessCreationByKey | ProcessCreationByVersionTag,
    **kwargs: Any,
) -> CreateProcessInstanceResult: ...
