from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_batch_operation_response_400 import (
    CancelBatchOperationResponse400,
)
from ...models.cancel_batch_operation_response_403 import (
    CancelBatchOperationResponse403,
)
from ...models.cancel_batch_operation_response_404 import (
    CancelBatchOperationResponse404,
)
from ...models.cancel_batch_operation_response_500 import (
    CancelBatchOperationResponse500,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    batch_operation_key: str, *, body: Any | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/batch-operations/{batch_operation_key}/cancellation".format(
            batch_operation_key=quote(str(batch_operation_key), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | CancelBatchOperationResponse400
    | CancelBatchOperationResponse403
    | CancelBatchOperationResponse404
    | CancelBatchOperationResponse500
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = CancelBatchOperationResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = CancelBatchOperationResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = CancelBatchOperationResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = CancelBatchOperationResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | CancelBatchOperationResponse400
    | CancelBatchOperationResponse403
    | CancelBatchOperationResponse404
    | CancelBatchOperationResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    batch_operation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: Any | Unset = UNSET,
) -> Response[
    Any
    | CancelBatchOperationResponse400
    | CancelBatchOperationResponse403
    | CancelBatchOperationResponse404
    | CancelBatchOperationResponse500
]:
    """Cancel Batch operation

     Cancels a running batch operation.
    This is done asynchronously, the progress can be tracked using the batch operation status endpoint
    (/batch-operations/{batchOperationKey}).

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.
        body (Any | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CancelBatchOperationResponse400 | CancelBatchOperationResponse403 | CancelBatchOperationResponse404 | CancelBatchOperationResponse500]
    """
    kwargs = _get_kwargs(batch_operation_key=batch_operation_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    batch_operation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: Any | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Cancel Batch operation

     Cancels a running batch operation.
    This is done asynchronously, the progress can be tracked using the batch operation status endpoint
    (/batch-operations/{batchOperationKey}).

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.
        body (Any | Unset):

    Raises:
        errors.CancelBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CancelBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CancelBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
        errors.CancelBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        batch_operation_key=batch_operation_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CancelBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CancelBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CancelBatchOperationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CancelBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    batch_operation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: Any | Unset = UNSET,
) -> Response[
    Any
    | CancelBatchOperationResponse400
    | CancelBatchOperationResponse403
    | CancelBatchOperationResponse404
    | CancelBatchOperationResponse500
]:
    """Cancel Batch operation

     Cancels a running batch operation.
    This is done asynchronously, the progress can be tracked using the batch operation status endpoint
    (/batch-operations/{batchOperationKey}).

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.
        body (Any | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CancelBatchOperationResponse400 | CancelBatchOperationResponse403 | CancelBatchOperationResponse404 | CancelBatchOperationResponse500]
    """
    kwargs = _get_kwargs(batch_operation_key=batch_operation_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    batch_operation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: Any | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Cancel Batch operation

     Cancels a running batch operation.
    This is done asynchronously, the progress can be tracked using the batch operation status endpoint
    (/batch-operations/{batchOperationKey}).

    Args:
        batch_operation_key (str): System-generated key for an batch operation. Example:
            2251799813684321.
        body (Any | Unset):

    Raises:
        errors.CancelBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CancelBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CancelBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
        errors.CancelBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        batch_operation_key=batch_operation_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CancelBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CancelBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CancelBatchOperationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CancelBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CancelBatchOperationResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
