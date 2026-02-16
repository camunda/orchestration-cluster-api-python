from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_search_query_result import (
    ProcessDefinitionSearchQueryResult,
)
from ...models.search_process_definitions_data import SearchProcessDefinitionsData
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: SearchProcessDefinitionsData | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionSearchQueryResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionSearchQueryResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: SearchProcessDefinitionsData | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionSearchQueryResult]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: SearchProcessDefinitionsData | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: SearchProcessDefinitionsData | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionSearchQueryResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: SearchProcessDefinitionsData | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionSearchQueryResult: ...
