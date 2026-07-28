from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.take_runtime_backup_request import TakeRuntimeBackupRequest
from ...models.take_runtime_backup_response import TakeRuntimeBackupResponse
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: TakeRuntimeBackupRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TakeRuntimeBackupResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | TakeRuntimeBackupResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: TakeRuntimeBackupRequest | Unset = UNSET
) -> Response[ProblemDetail | TakeRuntimeBackupResponse]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    **kwargs: Any,
) -> TakeRuntimeBackupResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: TakeRuntimeBackupRequest | Unset = UNSET
) -> Response[ProblemDetail | TakeRuntimeBackupResponse]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    **kwargs: Any,
) -> TakeRuntimeBackupResponse: ...
