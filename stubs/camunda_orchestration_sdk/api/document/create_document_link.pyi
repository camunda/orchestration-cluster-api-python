from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.document_link import DocumentLink
from ...models.document_link_request import DocumentLinkRequest
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    document_id: str,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> DocumentLink | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DocumentLink | ProblemDetail]: ...
def sync_detailed(
    document_id: str,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[DocumentLink | ProblemDetail]: ...
def sync(
    document_id: str,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentLink: ...
async def asyncio_detailed(
    document_id: str,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[DocumentLink | ProblemDetail]: ...
async def asyncio(
    document_id: str,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentLink: ...
