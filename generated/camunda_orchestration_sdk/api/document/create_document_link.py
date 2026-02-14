from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_link import DocumentLink
from ...models.document_link_request import DocumentLinkRequest
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    document_id: str,
    *,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["storeId"] = store_id
    params["contentHash"] = content_hash
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/documents/{document_id}/links".format(
            document_id=quote(str(document_id), safe="")
        ),
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DocumentLink | ProblemDetail | None:
    if response.status_code == 201:
        response_201 = DocumentLink.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DocumentLink | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[DocumentLink | ProblemDetail]:
    """Create document link

     Create a link to a document in the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):
        body (DocumentLinkRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentLink | ProblemDetail]
    """
    kwargs = _get_kwargs(
        document_id=document_id, body=body, store_id=store_id, content_hash=content_hash
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentLink:
    """Create document link

     Create a link to a document in the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):
        body (DocumentLinkRequest | Unset):

    Raises:
        errors.CreateDocumentLinkBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        DocumentLink"""
    response = sync_detailed(
        document_id=document_id,
        client=client,
        body=body,
        store_id=store_id,
        content_hash=content_hash,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateDocumentLinkBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DocumentLink, response.parsed)


async def asyncio_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[DocumentLink | ProblemDetail]:
    """Create document link

     Create a link to a document in the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):
        body (DocumentLinkRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentLink | ProblemDetail]
    """
    kwargs = _get_kwargs(
        document_id=document_id, body=body, store_id=store_id, content_hash=content_hash
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DocumentLinkRequest | Unset = UNSET,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> DocumentLink:
    """Create document link

     Create a link to a document in the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):
        body (DocumentLinkRequest | Unset):

    Raises:
        errors.CreateDocumentLinkBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        DocumentLink"""
    response = await asyncio_detailed(
        document_id=document_id,
        client=client,
        body=body,
        store_id=store_id,
        content_hash=content_hash,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateDocumentLinkBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DocumentLink, response.parsed)
