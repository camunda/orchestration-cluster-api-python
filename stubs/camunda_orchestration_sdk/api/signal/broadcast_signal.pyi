from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.signal_broadcast_request import SignalBroadcastRequest
from ...models.signal_broadcast_result import SignalBroadcastResult
from ...types import Response

def _get_kwargs(body: SignalBroadcastRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SignalBroadcastResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SignalBroadcastResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: SignalBroadcastRequest
) -> Response[ProblemDetail | SignalBroadcastResult]: ...
def sync(
    client: AuthenticatedClient | Client, body: SignalBroadcastRequest, **kwargs: Any
) -> SignalBroadcastResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: SignalBroadcastRequest
) -> Response[ProblemDetail | SignalBroadcastResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client, body: SignalBroadcastRequest, **kwargs: Any
) -> SignalBroadcastResult: ...
