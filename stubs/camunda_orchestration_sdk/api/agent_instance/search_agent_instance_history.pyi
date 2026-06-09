from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_history_search_query import (
    AgentInstanceHistorySearchQuery,
)
from ...models.agent_instance_history_search_query_result import (
    AgentInstanceHistorySearchQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    agent_instance_key: str, *, body: AgentInstanceHistorySearchQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceHistorySearchQueryResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceHistorySearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistorySearchQuery | Unset = UNSET,
) -> Response[AgentInstanceHistorySearchQueryResult | ProblemDetail]: ...
def sync(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistorySearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentInstanceHistorySearchQueryResult: ...
async def asyncio_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistorySearchQuery | Unset = UNSET,
) -> Response[AgentInstanceHistorySearchQueryResult | ProblemDetail]: ...
async def asyncio(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistorySearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> AgentInstanceHistorySearchQueryResult: ...
