from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.decision_definition_result import DecisionDefinitionResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(decision_definition_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> DecisionDefinitionResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DecisionDefinitionResult | ProblemDetail]: ...
def sync_detailed(
    decision_definition_key: str, client: AuthenticatedClient | Client
) -> Response[DecisionDefinitionResult | ProblemDetail]: ...
def sync(
    decision_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> DecisionDefinitionResult: ...
async def asyncio_detailed(
    decision_definition_key: str, client: AuthenticatedClient | Client
) -> Response[DecisionDefinitionResult | ProblemDetail]: ...
async def asyncio(
    decision_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> DecisionDefinitionResult: ...
