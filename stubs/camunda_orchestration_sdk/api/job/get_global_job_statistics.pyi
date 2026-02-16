import datetime
from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.global_job_statistics_query_result import GlobalJobStatisticsQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    from_: datetime.datetime, to: datetime.datetime, job_type: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> GlobalJobStatisticsQueryResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
    **kwargs: Any,
) -> GlobalJobStatisticsQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
    **kwargs: Any,
) -> GlobalJobStatisticsQueryResult: ...
