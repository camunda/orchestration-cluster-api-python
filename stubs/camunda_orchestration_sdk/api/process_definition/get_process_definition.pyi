from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_result import ProcessDefinitionResult
from ...types import Response

def _get_kwargs(process_definition_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionResult]: ...
def sync_detailed(
    process_definition_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ProcessDefinitionResult]: ...
def sync(
    process_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ProcessDefinitionResult: ...
async def asyncio_detailed(
    process_definition_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ProcessDefinitionResult]: ...
async def asyncio(
    process_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ProcessDefinitionResult: ...
