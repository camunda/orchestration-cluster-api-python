from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_topology_response import ClusterTopologyResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterTopologyResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterTopologyResponse | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ClusterTopologyResponse | ProblemDetail]: ...
def sync(*, client: AuthenticatedClient, **kwargs: Any) -> ClusterTopologyResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ClusterTopologyResponse | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> ClusterTopologyResponse: ...
