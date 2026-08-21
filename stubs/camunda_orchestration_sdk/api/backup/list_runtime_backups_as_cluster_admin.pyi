from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_runtime_backup_info import ClusterRuntimeBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, physical_tenant_id: str | Unset = UNSET, prefix: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[ClusterRuntimeBackupInfo] | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]: ...
def sync(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]: ...
