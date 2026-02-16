from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.incident_process_instance_statistics_by_definition_query import (
    IncidentProcessInstanceStatisticsByDefinitionQuery,
)
from ...models.incident_process_instance_statistics_by_definition_query_result import (
    IncidentProcessInstanceStatisticsByDefinitionQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(
    body: IncidentProcessInstanceStatisticsByDefinitionQuery,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    IncidentProcessInstanceStatisticsByDefinitionQueryResult | ProblemDetail | None
): ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    IncidentProcessInstanceStatisticsByDefinitionQueryResult | ProblemDetail
]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByDefinitionQuery,
) -> Response[
    IncidentProcessInstanceStatisticsByDefinitionQueryResult | ProblemDetail
]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByDefinitionQuery,
    **kwargs: Any,
) -> IncidentProcessInstanceStatisticsByDefinitionQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByDefinitionQuery,
) -> Response[
    IncidentProcessInstanceStatisticsByDefinitionQueryResult | ProblemDetail
]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: IncidentProcessInstanceStatisticsByDefinitionQuery,
    **kwargs: Any,
) -> IncidentProcessInstanceStatisticsByDefinitionQueryResult: ...
