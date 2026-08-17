from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_restore_request import ClusterRestoreRequest
from ...models.cluster_restore_response import ClusterRestoreResponse
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ClusterRestoreResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse: ...
