from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.backup_info import BackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(*, prefix: str | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[BackupInfo] | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | list[BackupInfo]]: ...
def sync_detailed(
    *, client: AuthenticatedClient, prefix: str | Unset = UNSET
) -> Response[ProblemDetail | list[BackupInfo]]: ...
def sync(
    *, client: AuthenticatedClient, prefix: str | Unset = UNSET, **kwargs: Any
) -> list[Any]: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, prefix: str | Unset = UNSET
) -> Response[ProblemDetail | list[BackupInfo]]: ...
async def asyncio(
    *, client: AuthenticatedClient, prefix: str | Unset = UNSET, **kwargs: Any
) -> list[Any]: ...
