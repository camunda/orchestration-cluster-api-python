from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_instance_statistics_query import (
    ProcessDefinitionInstanceStatisticsQuery,
)
from ...models.process_definition_instance_statistics_query_result import (
    ProcessDefinitionInstanceStatisticsQueryResult,
)
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionInstanceStatisticsQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionInstanceStatisticsQueryResult: ...
