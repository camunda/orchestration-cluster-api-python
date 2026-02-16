from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.get_process_definition_statistics_data import (
    GetProcessDefinitionStatisticsData,
)
from ...models.get_process_definition_statistics_response_200 import (
    GetProcessDefinitionStatisticsResponse200,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    process_definition_key: str,
    body: GetProcessDefinitionStatisticsData | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> GetProcessDefinitionStatisticsResponse200 | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetProcessDefinitionStatisticsResponse200 | ProblemDetail]: ...
def sync_detailed(
    process_definition_key: str,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionStatisticsData | Unset = UNSET,
) -> Response[GetProcessDefinitionStatisticsResponse200 | ProblemDetail]: ...
def sync(
    process_definition_key: str,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionStatisticsData | Unset = UNSET,
    **kwargs: Any,
) -> GetProcessDefinitionStatisticsResponse200: ...
async def asyncio_detailed(
    process_definition_key: str,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionStatisticsData | Unset = UNSET,
) -> Response[GetProcessDefinitionStatisticsResponse200 | ProblemDetail]: ...
async def asyncio(
    process_definition_key: str,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionStatisticsData | Unset = UNSET,
    **kwargs: Any,
) -> GetProcessDefinitionStatisticsResponse200: ...
