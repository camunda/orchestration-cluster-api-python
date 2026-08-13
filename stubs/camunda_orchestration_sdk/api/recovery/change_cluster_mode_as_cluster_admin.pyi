from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_mode_change_response import ClusterModeChangeResponse
from ...models.mode import Mode
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ClusterModeChangeResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse: ...
