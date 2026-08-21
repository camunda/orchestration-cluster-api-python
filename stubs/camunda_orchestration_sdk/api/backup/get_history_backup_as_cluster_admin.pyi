from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_history_backup_info import ClusterHistoryBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    backup_id: int, *, physical_tenant_id: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterHistoryBackupInfo | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterHistoryBackupInfo | ProblemDetail]: ...
def sync_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterHistoryBackupInfo | ProblemDetail]: ...
def sync(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterHistoryBackupInfo: ...
async def asyncio_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterHistoryBackupInfo | ProblemDetail]: ...
async def asyncio(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterHistoryBackupInfo: ...
