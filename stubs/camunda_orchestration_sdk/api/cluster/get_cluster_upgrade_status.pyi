from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.cluster_upgrade_status_response import ClusterUpgradeStatusResponse
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterUpgradeStatusResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterUpgradeStatusResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterUpgradeStatusResponse]: ...
def sync(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterUpgradeStatusResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterUpgradeStatusResponse]: ...
async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterUpgradeStatusResponse: ...
