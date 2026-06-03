from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_update_request import AgentInstanceUpdateRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(
    agent_instance_key: str, *, body: AgentInstanceUpdateRequest
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
) -> Response[Any | ProblemDetail]: ...
def sync(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
    **kwargs: Any,
) -> None: ...
