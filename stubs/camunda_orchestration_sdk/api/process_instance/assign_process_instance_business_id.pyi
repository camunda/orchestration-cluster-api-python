from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_instance_business_id_assignment_instruction import (
    ProcessInstanceBusinessIdAssignmentInstruction,
)
from ...types import Response

def _get_kwargs(
    process_instance_key: str, *, body: ProcessInstanceBusinessIdAssignmentInstruction
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    process_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessInstanceBusinessIdAssignmentInstruction,
) -> Response[Any | ProblemDetail]: ...
def sync(
    process_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessInstanceBusinessIdAssignmentInstruction,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    process_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessInstanceBusinessIdAssignmentInstruction,
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    process_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessInstanceBusinessIdAssignmentInstruction,
    **kwargs: Any,
) -> None: ...
