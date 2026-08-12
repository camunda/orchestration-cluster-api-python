from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_mode_change_response import ClusterModeChangeResponse
from ...models.problem_detail import ProblemDetail
from ...models.restore_request import RestoreRequest
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ClusterModeChangeResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: RestoreRequest,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RestoreRequest,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
