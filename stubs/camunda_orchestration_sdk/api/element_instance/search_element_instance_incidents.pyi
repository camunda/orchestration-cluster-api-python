from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.incident_search_query import IncidentSearchQuery
from ...models.incident_search_query_result import IncidentSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    element_instance_key: str, *, body: IncidentSearchQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> IncidentSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[IncidentSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    element_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: IncidentSearchQuery | Unset = UNSET,
) -> Response[IncidentSearchQueryResult | ProblemDetail]: ...
def sync(
    element_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: IncidentSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> IncidentSearchQueryResult: ...
async def asyncio_detailed(
    element_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: IncidentSearchQuery | Unset = UNSET,
) -> Response[IncidentSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    element_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: IncidentSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> IncidentSearchQueryResult: ...
