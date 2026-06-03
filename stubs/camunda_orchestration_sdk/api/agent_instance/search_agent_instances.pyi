from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_search_query import AgentInstanceSearchQuery
from ...models.agent_instance_search_query_result import AgentInstanceSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: AgentInstanceSearchQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: AgentInstanceSearchQuery | Unset = UNSET
) -> Response[AgentInstanceSearchQueryResult | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: AgentInstanceSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentInstanceSearchQueryResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: AgentInstanceSearchQuery | Unset = UNSET
) -> Response[AgentInstanceSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AgentInstanceSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentInstanceSearchQueryResult: ...
