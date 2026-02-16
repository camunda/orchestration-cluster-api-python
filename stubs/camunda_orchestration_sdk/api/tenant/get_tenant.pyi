from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.tenant_result import TenantResult
from ...types import Response

def _get_kwargs(tenant_id: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | TenantResult]: ...
def sync_detailed(
    tenant_id: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | TenantResult]: ...
def sync(
    tenant_id: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> TenantResult: ...
async def asyncio_detailed(
    tenant_id: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | TenantResult]: ...
async def asyncio(
    tenant_id: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> TenantResult: ...
