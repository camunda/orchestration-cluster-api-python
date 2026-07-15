from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_variable_name_search_query import (
    ProcessDefinitionVariableNameSearchQuery,
)
from ...models.process_definition_variable_name_search_query_result import (
    ProcessDefinitionVariableNameSearchQueryResult,
)
from ...types import UNSET, Response, Unset

def _get_kwargs(
    process_definition_key: str,
    *,
    body: ProcessDefinitionVariableNameSearchQuery | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionVariableNameSearchQueryResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionVariableNameSearchQueryResult]: ...
def sync_detailed(
    process_definition_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionVariableNameSearchQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionVariableNameSearchQueryResult]: ...
def sync(
    process_definition_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionVariableNameSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionVariableNameSearchQueryResult: ...
async def asyncio_detailed(
    process_definition_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionVariableNameSearchQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionVariableNameSearchQueryResult]: ...
async def asyncio(
    process_definition_key: str,
    *,
    client: AuthenticatedClient,
    body: ProcessDefinitionVariableNameSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionVariableNameSearchQueryResult: ...
