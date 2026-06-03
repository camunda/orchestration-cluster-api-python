from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.clock_pin_request import ClockPinRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(*, body: ClockPinRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: ClockPinRequest
) -> Response[Any | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, body: ClockPinRequest, **kwargs: Any
) -> None: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ClockPinRequest
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: ClockPinRequest, **kwargs: Any
) -> None: ...
