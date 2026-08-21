from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(*, soft: bool | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    *, client: AuthenticatedClient, soft: bool | Unset = UNSET
) -> Response[Any | ProblemDetail]: ...
def sync(
    *, client: AuthenticatedClient, soft: bool | Unset = UNSET, **kwargs: Any
) -> None: ...
async def asyncio_detailed(
    *, client: AuthenticatedClient, soft: bool | Unset = UNSET
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    *, client: AuthenticatedClient, soft: bool | Unset = UNSET, **kwargs: Any
) -> None: ...
