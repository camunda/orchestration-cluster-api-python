from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(*, physical_tenant_id: str | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, physical_tenant_id: str | Unset = UNSET
) -> Response[Any | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, physical_tenant_id: str | Unset = UNSET
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> None: ...
