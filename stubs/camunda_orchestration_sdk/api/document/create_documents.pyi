from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.create_documents_data import CreateDocumentsData
from ...models.document_creation_batch_response import DocumentCreationBatchResponse
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    body: CreateDocumentsData, store_id: str | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> DocumentCreationBatchResponse | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DocumentCreationBatchResponse | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client,
    body: CreateDocumentsData,
    store_id: str | Unset = UNSET,
) -> Response[DocumentCreationBatchResponse | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: CreateDocumentsData,
    store_id: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentCreationBatchResponse: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client,
    body: CreateDocumentsData,
    store_id: str | Unset = UNSET,
) -> Response[DocumentCreationBatchResponse | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: CreateDocumentsData,
    store_id: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentCreationBatchResponse: ...
