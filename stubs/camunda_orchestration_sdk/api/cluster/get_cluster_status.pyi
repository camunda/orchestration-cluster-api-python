from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_status_response import ClusterStatusResponse
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterStatusResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterStatusResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterStatusResponse]: ...
def sync(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterStatusResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterStatusResponse]: ...
async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterStatusResponse: ...
