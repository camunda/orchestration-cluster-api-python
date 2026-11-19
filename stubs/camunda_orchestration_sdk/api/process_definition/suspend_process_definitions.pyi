from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_suspension_by_id import (
    ProcessDefinitionSuspensionByID,
)
from ...models.process_definition_suspension_by_key import (
    ProcessDefinitionSuspensionByKey,
)
from ...models.process_definition_suspension_result import (
    ProcessDefinitionSuspensionResult,
)
from ...types import Response

def _get_kwargs(
    *, body: ProcessDefinitionSuspensionByID | ProcessDefinitionSuspensionByKey
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionSuspensionResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionSuspensionResult]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionSuspensionByID | ProcessDefinitionSuspensionByKey,
) -> Response[ProblemDetail | ProcessDefinitionSuspensionResult]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionSuspensionByID | ProcessDefinitionSuspensionByKey,
    **kwargs: Any,
) -> ProcessDefinitionSuspensionResult: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionSuspensionByID | ProcessDefinitionSuspensionByKey,
) -> Response[ProblemDetail | ProcessDefinitionSuspensionResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionSuspensionByID | ProcessDefinitionSuspensionByKey,
    **kwargs: Any,
) -> ProcessDefinitionSuspensionResult: ...
