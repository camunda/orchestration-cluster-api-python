from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.rebalance_cancellation_response import RebalanceCancellationResponse
from ...types import Response

def _get_kwargs() -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RebalanceCancellationResponse | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RebalanceCancellationResponse]: ...
def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RebalanceCancellationResponse]: ...
def sync(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RebalanceCancellationResponse: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RebalanceCancellationResponse]: ...
async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RebalanceCancellationResponse: ...
