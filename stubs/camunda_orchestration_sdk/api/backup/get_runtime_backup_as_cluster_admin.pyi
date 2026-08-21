from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_runtime_backup_info import ClusterRuntimeBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    backup_id: int, *, physical_tenant_id: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterRuntimeBackupInfo | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterRuntimeBackupInfo | ProblemDetail]: ...
def sync_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterRuntimeBackupInfo | ProblemDetail]: ...
def sync(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRuntimeBackupInfo: ...
async def asyncio_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterRuntimeBackupInfo | ProblemDetail]: ...
async def asyncio(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRuntimeBackupInfo: ...
