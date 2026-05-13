from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.form_result import FormResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(form_key: str) -> dict[str, Any]: ...
def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FormResult | ProblemDetail | None: ...
def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FormResult | ProblemDetail]: ...
def sync_detailed(
    form_key: str, *, client: AuthenticatedClient | Client
) -> Response[FormResult | ProblemDetail]: ...
def sync(
    form_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> FormResult: ...
async def asyncio_detailed(
    form_key: str, *, client: AuthenticatedClient | Client
) -> Response[FormResult | ProblemDetail]: ...
async def asyncio(
    form_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> FormResult: ...
