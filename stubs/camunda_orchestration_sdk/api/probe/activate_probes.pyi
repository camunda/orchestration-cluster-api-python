from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.probe_activation_request import ProbeActivationRequest
from ...models.probe_activation_result import ProbeActivationResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(*, body: ProbeActivationRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProbeActivationResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProbeActivationResult | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: ProbeActivationRequest
) -> Response[ProbeActivationResult | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, body: ProbeActivationRequest, **kwargs: Any
) -> ProbeActivationResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ProbeActivationRequest
) -> Response[ProbeActivationResult | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: ProbeActivationRequest, **kwargs: Any
) -> ProbeActivationResult: ...
