from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.get_start_process_form_response_200 import GetStartProcessFormResponse200
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(process_definition_key: str) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GetStartProcessFormResponse200 | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | GetStartProcessFormResponse200 | ProblemDetail]: ...
def sync_detailed(
    process_definition_key: str, client: AuthenticatedClient | Client
) -> Response[Any | GetStartProcessFormResponse200 | ProblemDetail]: ...
def sync(
    process_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetStartProcessFormResponse200: ...
async def asyncio_detailed(
    process_definition_key: str, client: AuthenticatedClient | Client
) -> Response[Any | GetStartProcessFormResponse200 | ProblemDetail]: ...
async def asyncio(
    process_definition_key: str, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetStartProcessFormResponse200: ...
