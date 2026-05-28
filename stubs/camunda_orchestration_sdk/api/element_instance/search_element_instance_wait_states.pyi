from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.element_instance_wait_state_query import ElementInstanceWaitStateQuery
from ...models.element_instance_wait_state_query_result import (
    ElementInstanceWaitStateQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    *, body: ElementInstanceWaitStateQuery | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ElementInstanceWaitStateQueryResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ElementInstanceWaitStateQueryResult | ProblemDetail]: ...
def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ElementInstanceWaitStateQuery | Unset = UNSET,
) -> Response[ElementInstanceWaitStateQueryResult | ProblemDetail]: ...
def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ElementInstanceWaitStateQuery | Unset = UNSET,
    **kwargs: Any,
) -> ElementInstanceWaitStateQueryResult: ...
async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ElementInstanceWaitStateQuery | Unset = UNSET,
) -> Response[ElementInstanceWaitStateQueryResult | ProblemDetail]: ...
async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ElementInstanceWaitStateQuery | Unset = UNSET,
    **kwargs: Any,
) -> ElementInstanceWaitStateQueryResult: ...
