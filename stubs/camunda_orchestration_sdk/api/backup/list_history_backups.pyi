from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.history_backup_info import HistoryBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, prefix: str | Unset = UNSET, verbose: bool | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[HistoryBackupInfo] | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | list[HistoryBackupInfo]]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
) -> Response[ProblemDetail | list[HistoryBackupInfo]]: ...
def sync(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
) -> Response[ProblemDetail | list[HistoryBackupInfo]]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]: ...
