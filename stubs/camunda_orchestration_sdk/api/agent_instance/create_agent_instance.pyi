from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_creation_request import AgentInstanceCreationRequest
from ...models.agent_instance_creation_result import AgentInstanceCreationResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(*, body: AgentInstanceCreationRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceCreationResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceCreationResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: AgentInstanceCreationRequest
) -> Response[AgentInstanceCreationResult | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, body: AgentInstanceCreationRequest, **kwargs: Any
) -> AgentInstanceCreationResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: AgentInstanceCreationRequest
) -> Response[AgentInstanceCreationResult | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: AgentInstanceCreationRequest, **kwargs: Any
) -> AgentInstanceCreationResult: ...
