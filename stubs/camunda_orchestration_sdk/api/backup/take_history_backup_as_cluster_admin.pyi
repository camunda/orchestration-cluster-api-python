from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_take_history_backup_response import (
    ClusterTakeHistoryBackupResponse,
)
from ...models.problem_detail import ProblemDetail
from ...models.take_history_backup_request import TakeHistoryBackupRequest
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: TakeHistoryBackupRequest, physical_tenant_id: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterTakeHistoryBackupResponse | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeHistoryBackupResponse: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeHistoryBackupResponse: ...
