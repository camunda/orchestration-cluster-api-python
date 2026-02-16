from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(group_id: str, mapping_rule_id: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    group_id: str, mapping_rule_id: str, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]: ...
def sync(
    group_id: str,
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    group_id: str, mapping_rule_id: str, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    group_id: str,
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> None: ...
