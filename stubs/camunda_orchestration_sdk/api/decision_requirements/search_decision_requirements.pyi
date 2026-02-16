from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.decision_requirements_search_query import DecisionRequirementsSearchQuery
from ...models.decision_requirements_search_query_result import (
    DecisionRequirementsSearchQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: DecisionRequirementsSearchQuery | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> DecisionRequirementsSearchQueryResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DecisionRequirementsSearchQueryResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: DecisionRequirementsSearchQuery | Unset = UNSET,
) -> Response[DecisionRequirementsSearchQueryResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: DecisionRequirementsSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> DecisionRequirementsSearchQueryResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: DecisionRequirementsSearchQuery | Unset = UNSET,
) -> Response[DecisionRequirementsSearchQueryResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: DecisionRequirementsSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> DecisionRequirementsSearchQueryResult: ...
