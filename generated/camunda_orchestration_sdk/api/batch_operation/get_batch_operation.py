from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_response import BatchOperationResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(batch_operation_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/batch-operations/{batch_operation_key}".format(
            batch_operation_key=quote(str(batch_operation_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationResponse | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = BatchOperationResponse.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
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
) -> Response[BatchOperationResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    batch_operation_key: str, *, client: AuthenticatedClient | Client
) -> Response[BatchOperationResponse | ProblemDetail]:
    """Get batch operation

     Get batch operation by key.

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(batch_operation_key=batch_operation_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    batch_operation_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationResponse:
    """Get batch operation

     Get batch operation by key.

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.

    Raises:
        errors.GetBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetBatchOperationNotFound: If the response status code is 404. The batch operation is not found.
        errors.GetBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationResponse"""
    response = sync_detailed(batch_operation_key=batch_operation_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetBatchOperationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationResponse, response.parsed)


async def asyncio_detailed(
    batch_operation_key: str, *, client: AuthenticatedClient | Client
) -> Response[BatchOperationResponse | ProblemDetail]:
    """Get batch operation

     Get batch operation by key.

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(batch_operation_key=batch_operation_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    batch_operation_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> BatchOperationResponse:
    """Get batch operation

     Get batch operation by key.

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.

    Raises:
        errors.GetBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetBatchOperationNotFound: If the response status code is 404. The batch operation is not found.
        errors.GetBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationResponse"""
    response = await asyncio_detailed(
        batch_operation_key=batch_operation_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetBatchOperationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationResponse, response.parsed)
