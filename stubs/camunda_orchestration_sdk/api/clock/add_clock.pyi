from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.clock_add_request import ClockAddRequest
from ...models.clock_result import ClockResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(*, body: ClockAddRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClockResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClockResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: ClockAddRequest
) -> Response[ClockResult | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, body: ClockAddRequest, **kwargs: Any
) -> ClockResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ClockAddRequest
) -> Response[ClockResult | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: ClockAddRequest, **kwargs: Any
) -> ClockResult: ...
