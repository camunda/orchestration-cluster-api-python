from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_balance_response import ClusterBalanceResponse
from ...models.cluster_rebalance_request import ClusterRebalanceRequest
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: ClusterRebalanceRequest | Unset = UNSET, dry_run: bool | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterBalanceResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterBalanceResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterBalanceResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterBalanceResponse: ...
