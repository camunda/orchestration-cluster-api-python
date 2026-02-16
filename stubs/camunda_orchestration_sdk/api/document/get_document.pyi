from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, File, Response, Unset

def _get_kwargs(
    document_id: str, store_id: str | Unset = UNSET, content_hash: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> File | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[File | ProblemDetail]: ...
def sync_detailed(
    document_id: str,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[File | ProblemDetail]: ...
def sync(
    document_id: str,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> File: ...
async def asyncio_detailed(
    document_id: str,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[File | ProblemDetail]: ...
async def asyncio(
    document_id: str,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> File: ...
