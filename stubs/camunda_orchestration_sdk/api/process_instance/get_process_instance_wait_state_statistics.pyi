from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_instance_wait_state_statistics_query_result import (
    ProcessInstanceWaitStateStatisticsQueryResult,
)
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessInstanceWaitStateStatisticsQueryResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | ProcessInstanceWaitStateStatisticsQueryResult]: ...
def sync_detailed(
    process_instance_key: str, *, client: AuthenticatedClient
) -> Response[ProblemDetail | ProcessInstanceWaitStateStatisticsQueryResult]: ...
def sync(
    process_instance_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> ProcessInstanceWaitStateStatisticsQueryResult: ...
async def asyncio_detailed(
    process_instance_key: str, *, client: AuthenticatedClient
) -> Response[ProblemDetail | ProcessInstanceWaitStateStatisticsQueryResult]: ...
async def asyncio(
    process_instance_key: str, *, client: AuthenticatedClient, **kwargs: Any
) -> ProcessInstanceWaitStateStatisticsQueryResult: ...
