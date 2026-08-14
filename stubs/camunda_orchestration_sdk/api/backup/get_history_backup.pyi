from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.history_backup_info import HistoryBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(backup_id: int) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HistoryBackupInfo | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HistoryBackupInfo | ProblemDetail]: ...
def sync_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[HistoryBackupInfo | ProblemDetail]: ...
def sync(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> HistoryBackupInfo: ...
async def asyncio_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[HistoryBackupInfo | ProblemDetail]: ...
async def asyncio(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> HistoryBackupInfo: ...
