from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.backup_info import BackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(backup_id: int) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BackupInfo | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BackupInfo | ProblemDetail]: ...
def sync_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[BackupInfo | ProblemDetail]: ...
def sync(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> BackupInfo: ...
async def asyncio_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[BackupInfo | ProblemDetail]: ...
async def asyncio(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> BackupInfo: ...
