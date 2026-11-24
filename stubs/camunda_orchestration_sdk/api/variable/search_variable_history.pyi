from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.variable_history_item_search_query import VariableHistoryItemSearchQuery
from ...models.variable_history_item_search_query_result import (
    VariableHistoryItemSearchQueryResult,
)
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableHistoryItemSearchQueryResult | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]: ...
def sync(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableHistoryItemSearchQueryResult: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]: ...
async def asyncio(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableHistoryItemSearchQueryResult: ...
