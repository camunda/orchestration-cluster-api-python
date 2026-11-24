from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.error_probe_result import ErrorProbeResult
from ...models.ok_probe_result import OKProbeResult
from ...models.probe_creation_request import ProbeCreationRequest
from ...models.problem_detail import ProblemDetail
from ...models.unsupported_probe_result import UnsupportedProbeResult
from ...types import Response

def _get_kwargs(*, body: ProbeCreationRequest) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail | None
): ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]: ...
def sync_detailed(
    *, client: AuthenticatedClient, body: ProbeCreationRequest
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]: ...
def sync(
    *, client: AuthenticatedClient, body: ProbeCreationRequest, **kwargs: Any
) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ProbeCreationRequest
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]: ...
async def asyncio(
    *, client: AuthenticatedClient, body: ProbeCreationRequest, **kwargs: Any
) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult: ...
