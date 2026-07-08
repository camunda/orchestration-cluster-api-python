from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.change_cluster_mode_mode import ChangeClusterModeMode
from ...models.cluster_mode_change_response import ClusterModeChangeResponse
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, mode: ChangeClusterModeMode, dry_run: bool | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterModeChangeResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterModeChangeResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterModeChangeResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterModeChangeResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
