from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.secret_list_request import SecretListRequest
from ...models.secret_list_result import SecretListResult
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SecretListRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SecretListResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SecretListResult]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: SecretListRequest | Unset = UNSET
) -> Response[ProblemDetail | SecretListResult]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: SecretListRequest | Unset = UNSET,
    **kwargs: Any,
) -> SecretListResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: SecretListRequest | Unset = UNSET
) -> Response[ProblemDetail | SecretListResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SecretListRequest | Unset = UNSET,
    **kwargs: Any,
) -> SecretListResult: ...
