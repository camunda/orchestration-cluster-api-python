from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_resumption_by_id import (
    ProcessDefinitionResumptionByID,
)
from ...models.process_definition_resumption_by_key import (
    ProcessDefinitionResumptionByKey,
)
from ...models.process_definition_resumption_result import (
    ProcessDefinitionResumptionResult,
)
from ...types import Response

def _get_kwargs(
    *, body: ProcessDefinitionResumptionByID | ProcessDefinitionResumptionByKey
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionResumptionResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionResumptionResult]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionResumptionByID | ProcessDefinitionResumptionByKey,
) -> Response[ProblemDetail | ProcessDefinitionResumptionResult]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionResumptionByID | ProcessDefinitionResumptionByKey,
    **kwargs: Any,
) -> ProcessDefinitionResumptionResult: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionResumptionByID | ProcessDefinitionResumptionByKey,
) -> Response[ProblemDetail | ProcessDefinitionResumptionResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionResumptionByID | ProcessDefinitionResumptionByKey,
    **kwargs: Any,
) -> ProcessDefinitionResumptionResult: ...
