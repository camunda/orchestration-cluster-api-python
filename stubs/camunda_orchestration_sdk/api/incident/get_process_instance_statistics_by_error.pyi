from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.incident_process_instance_statistics_by_error_query import (
    IncidentProcessInstanceStatisticsByErrorQuery,
)
from ...models.incident_process_instance_statistics_by_error_query_result import (
    IncidentProcessInstanceStatisticsByErrorQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> IncidentProcessInstanceStatisticsByErrorQueryResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[IncidentProcessInstanceStatisticsByErrorQueryResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
) -> Response[IncidentProcessInstanceStatisticsByErrorQueryResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
    **kwargs: Any,
) -> IncidentProcessInstanceStatisticsByErrorQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
) -> Response[IncidentProcessInstanceStatisticsByErrorQueryResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
    **kwargs: Any,
) -> IncidentProcessInstanceStatisticsByErrorQueryResult: ...
