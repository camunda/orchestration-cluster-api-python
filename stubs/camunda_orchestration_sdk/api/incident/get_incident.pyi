from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.incident_result import IncidentResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(incident_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> IncidentResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[IncidentResult | ProblemDetail]: ...
def sync_detailed(
    incident_key: str, client: AuthenticatedClient | Client
) -> Response[IncidentResult | ProblemDetail]: ...
def sync(
    incident_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> IncidentResult: ...
async def asyncio_detailed(
    incident_key: str, client: AuthenticatedClient | Client
) -> Response[IncidentResult | ProblemDetail]: ...
async def asyncio(
    incident_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> IncidentResult: ...
