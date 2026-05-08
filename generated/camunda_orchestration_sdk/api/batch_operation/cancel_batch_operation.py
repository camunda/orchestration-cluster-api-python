from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
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
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
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
) -> Response[Any | ProblemDetail]:
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
) -> Response[Any | ProblemDetail]:
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
        Response[Any | ProblemDetail]
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
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. Not found. The batch operation was not found.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        batch_operation_key=batch_operation_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="cancel_batch_operation",
        )
    return None


async def asyncio_detailed(
    batch_operation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: Any | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
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
        Response[Any | ProblemDetail]
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
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. Not found. The batch operation was not found.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        batch_operation_key=batch_operation_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_batch_operation",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="cancel_batch_operation",
        )
    return None
