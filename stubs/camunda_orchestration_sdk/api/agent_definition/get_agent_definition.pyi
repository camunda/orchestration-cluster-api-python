from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.agent_definition_result import AgentDefinitionResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(agent_definition_key: str) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentDefinitionResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentDefinitionResult | ProblemDetail]: ...
def sync_detailed(
    agent_definition_key: str, *, client: AuthenticatedClient
) -> Response[AgentDefinitionResult | ProblemDetail]: ...
def sync(
    agent_definition_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> AgentDefinitionResult: ...
async def asyncio_detailed(
    agent_definition_key: str, *, client: AuthenticatedClient
) -> Response[AgentDefinitionResult | ProblemDetail]: ...
async def asyncio(
    agent_definition_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> AgentDefinitionResult: ...
