from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_user_task_variables_data import SearchUserTaskVariablesData
from ...models.variable_search_query_result import VariableSearchQueryResult
from ...types import UNSET, Response, Unset

def _get_kwargs(
    user_task_key: str,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableSearchQueryResult | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | VariableSearchQueryResult]: ...
def sync_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]: ...
def sync(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult: ...
async def asyncio_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]: ...
async def asyncio(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult: ...
