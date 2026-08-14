from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.take_history_backup_request import TakeHistoryBackupRequest
from ...models.take_history_backup_response import TakeHistoryBackupResponse
from ...types import Response

def _get_kwargs(*, body: TakeHistoryBackupRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TakeHistoryBackupResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | TakeHistoryBackupResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest
) -> Response[ProblemDetail | TakeHistoryBackupResponse]: ...
def sync(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest, **kwargs: Any
) -> TakeHistoryBackupResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest
) -> Response[ProblemDetail | TakeHistoryBackupResponse]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest, **kwargs: Any
) -> TakeHistoryBackupResponse: ...
