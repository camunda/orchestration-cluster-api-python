from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_message_subscription_statistics_query import (
    ProcessDefinitionMessageSubscriptionStatisticsQuery,
)
from ...models.process_definition_message_subscription_statistics_query_result import (
    ProcessDefinitionMessageSubscriptionStatisticsQueryResult,
)
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ProblemDetail | ProcessDefinitionMessageSubscriptionStatisticsQueryResult | None
): ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ProblemDetail | ProcessDefinitionMessageSubscriptionStatisticsQueryResult
]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
) -> Response[
    ProblemDetail | ProcessDefinitionMessageSubscriptionStatisticsQueryResult
]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionMessageSubscriptionStatisticsQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
) -> Response[
    ProblemDetail | ProcessDefinitionMessageSubscriptionStatisticsQueryResult
]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionMessageSubscriptionStatisticsQueryResult: ...
