from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.runtime_backup_state import RuntimeBackupState
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RuntimeBackupState | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RuntimeBackupState]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RuntimeBackupState]: ...
def sync(*, client: AuthenticatedClient, **kwargs: Any) -> RuntimeBackupState: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RuntimeBackupState]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RuntimeBackupState: ...
