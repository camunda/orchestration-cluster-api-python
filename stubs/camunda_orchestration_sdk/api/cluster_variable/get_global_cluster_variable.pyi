from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_variable_result import ClusterVariableResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(name: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterVariableResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterVariableResult | ProblemDetail]: ...
def sync_detailed(
    name: str, client: AuthenticatedClient | Client
) -> Response[ClusterVariableResult | ProblemDetail]: ...
def sync(
    name: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterVariableResult: ...
async def asyncio_detailed(
    name: str, client: AuthenticatedClient | Client
) -> Response[ClusterVariableResult | ProblemDetail]: ...
async def asyncio(
    name: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterVariableResult: ...
