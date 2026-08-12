from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_definition_search_query import AgentDefinitionSearchQuery
from ...models.agent_definition_search_query_result import (
    AgentDefinitionSearchQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: AgentDefinitionSearchQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentDefinitionSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentDefinitionSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: AgentDefinitionSearchQuery | Unset = UNSET
) -> Response[AgentDefinitionSearchQueryResult | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: AgentDefinitionSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentDefinitionSearchQueryResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: AgentDefinitionSearchQuery | Unset = UNSET
) -> Response[AgentDefinitionSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AgentDefinitionSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentDefinitionSearchQueryResult: ...
