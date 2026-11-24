from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.error_probe_answer import ErrorProbeAnswer
from ...models.ok_probe_answer import OKProbeAnswer
from ...models.problem_detail import ProblemDetail
from ...models.unsupported_probe_answer import UnsupportedProbeAnswer
from ...types import Response

def _get_kwargs(
    probe_key: str, *, body: ErrorProbeAnswer | OKProbeAnswer | UnsupportedProbeAnswer
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    probe_key: str,
    *,
    client: AuthenticatedClient,
    body: ErrorProbeAnswer | OKProbeAnswer | UnsupportedProbeAnswer,
) -> Response[Any | ProblemDetail]: ...
def sync(
    probe_key: str,
    *,
    client: AuthenticatedClient,
    body: ErrorProbeAnswer | OKProbeAnswer | UnsupportedProbeAnswer,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    probe_key: str,
    *,
    client: AuthenticatedClient,
    body: ErrorProbeAnswer | OKProbeAnswer | UnsupportedProbeAnswer,
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    probe_key: str,
    *,
    client: AuthenticatedClient,
    body: ErrorProbeAnswer | OKProbeAnswer | UnsupportedProbeAnswer,
    **kwargs: Any,
) -> None: ...
