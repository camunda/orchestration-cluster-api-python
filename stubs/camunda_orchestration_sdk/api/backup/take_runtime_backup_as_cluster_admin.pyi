from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_take_runtime_backup_response import (
    ClusterTakeRuntimeBackupResponse,
)
from ...models.problem_detail import ProblemDetail
from ...models.take_runtime_backup_request import TakeRuntimeBackupRequest
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterTakeRuntimeBackupResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeRuntimeBackupResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeRuntimeBackupResponse: ...
