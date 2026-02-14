from http import HTTPStatus
from io import BytesIO
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    document_id: str,
    *,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params["storeId"] = store_id
    params["contentHash"] = content_hash
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents/{document_id}".format(
            document_id=quote(str(document_id), safe="")
        ),
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> File | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))
        return response_200
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[File | ProblemDetail]:
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
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[File | ProblemDetail]:
    """Download document

     Download a document from the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
    production), local (non-production)

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | ProblemDetail]
    """
    kwargs = _get_kwargs(
        document_id=document_id, store_id=store_id, content_hash=content_hash
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> File:
    """Download document

     Download a document from the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
    production), local (non-production)

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):

    Raises:
        errors.GetDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
        errors.GetDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        File"""
    response = sync_detailed(
        document_id=document_id,
        client=client,
        store_id=store_id,
        content_hash=content_hash,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetDocumentNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDocumentInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(File, response.parsed)


async def asyncio_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
) -> Response[File | ProblemDetail]:
    """Download document

     Download a document from the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
    production), local (non-production)

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | ProblemDetail]
    """
    kwargs = _get_kwargs(
        document_id=document_id, store_id=store_id, content_hash=content_hash
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    store_id: str | Unset = UNSET,
    content_hash: str | Unset = UNSET,
    **kwargs: Any,
) -> File:
    """Download document

     Download a document from the Camunda 8 cluster.

    Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
    production), local (non-production)

    Args:
        document_id (str): Document Id that uniquely identifies a document.
        store_id (str | Unset):
        content_hash (str | Unset):

    Raises:
        errors.GetDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
        errors.GetDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        File"""
    response = await asyncio_detailed(
        document_id=document_id,
        client=client,
        store_id=store_id,
        content_hash=content_hash,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetDocumentNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDocumentInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(File, response.parsed)
