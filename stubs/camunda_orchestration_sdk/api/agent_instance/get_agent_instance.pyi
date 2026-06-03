from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_result import AgentInstanceResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(agent_instance_key: str) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceResult | ProblemDetail]: ...
def sync_detailed(
    agent_instance_key: str, *, client: AuthenticatedClient
) -> Response[AgentInstanceResult | ProblemDetail]: ...
def sync(
    agent_instance_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> AgentInstanceResult: ...
async def asyncio_detailed(
    agent_instance_key: str, *, client: AuthenticatedClient
) -> Response[AgentInstanceResult | ProblemDetail]: ...
async def asyncio(
    agent_instance_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> AgentInstanceResult: ...
