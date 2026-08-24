from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_balance_response import ClusterBalanceResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterBalanceResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
def sync(*, client: AuthenticatedClient, **kwargs: Any) -> ClusterBalanceResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> ClusterBalanceResponse: ...
