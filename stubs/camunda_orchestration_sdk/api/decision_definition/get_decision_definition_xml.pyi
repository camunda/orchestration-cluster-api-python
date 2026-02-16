from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(decision_definition_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | str | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | str]: ...
def sync_detailed(
    decision_definition_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | str]: ...
def sync(
    decision_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> str: ...
async def asyncio_detailed(
    decision_definition_key: str, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | str]: ...
async def asyncio(
    decision_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> str: ...
