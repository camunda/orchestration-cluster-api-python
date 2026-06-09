from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_history_item_creation_result import (
    AgentInstanceHistoryItemCreationResult,
)
from ...models.agent_instance_history_item_request import (
    AgentInstanceHistoryItemRequest,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(
    agent_instance_key: str, *, body: AgentInstanceHistoryItemRequest
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceHistoryItemCreationResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceHistoryItemCreationResult | ProblemDetail]: ...
def sync_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistoryItemRequest,
) -> Response[AgentInstanceHistoryItemCreationResult | ProblemDetail]: ...
def sync(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistoryItemRequest,
    **kwargs: Any,
) -> AgentInstanceHistoryItemCreationResult: ...
async def asyncio_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistoryItemRequest,
) -> Response[AgentInstanceHistoryItemCreationResult | ProblemDetail]: ...
async def asyncio(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceHistoryItemRequest,
    **kwargs: Any,
) -> AgentInstanceHistoryItemCreationResult: ...
