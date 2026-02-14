from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.correlate_message_data import CorrelateMessageData
from ...models.correlate_message_response_200 import CorrelateMessageResponse200
from ...models.correlate_message_response_400 import CorrelateMessageResponse400
from ...models.correlate_message_response_403 import CorrelateMessageResponse403
from ...models.correlate_message_response_404 import CorrelateMessageResponse404
from ...models.correlate_message_response_500 import CorrelateMessageResponse500
from ...models.correlate_message_response_503 import CorrelateMessageResponse503
from ...types import Response


def _get_kwargs(*, body: CorrelateMessageData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/messages/correlation"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CorrelateMessageResponse200
    | CorrelateMessageResponse400
    | CorrelateMessageResponse403
    | CorrelateMessageResponse404
    | CorrelateMessageResponse500
    | CorrelateMessageResponse503
    | None
):
    if response.status_code == 200:
        response_200 = CorrelateMessageResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = CorrelateMessageResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = CorrelateMessageResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = CorrelateMessageResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = CorrelateMessageResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CorrelateMessageResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CorrelateMessageResponse200
    | CorrelateMessageResponse400
    | CorrelateMessageResponse403
    | CorrelateMessageResponse404
    | CorrelateMessageResponse500
    | CorrelateMessageResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: CorrelateMessageData
) -> Response[
    CorrelateMessageResponse200
    | CorrelateMessageResponse400
    | CorrelateMessageResponse403
    | CorrelateMessageResponse404
    | CorrelateMessageResponse500
    | CorrelateMessageResponse503
]:
    """Correlate message

     Publishes a message and correlates it to a subscription.
    If correlation is successful it will return the first process instance key the message correlated
    with.
    The message is not buffered.
    Use the publish message endpoint to send messages that can be buffered.

    Args:
        body (CorrelateMessageData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorrelateMessageResponse200 | CorrelateMessageResponse400 | CorrelateMessageResponse403 | CorrelateMessageResponse404 | CorrelateMessageResponse500 | CorrelateMessageResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, body: CorrelateMessageData, **kwargs: Any
) -> CorrelateMessageResponse200:
    """Correlate message

     Publishes a message and correlates it to a subscription.
    If correlation is successful it will return the first process instance key the message correlated
    with.
    The message is not buffered.
    Use the publish message endpoint to send messages that can be buffered.

    Args:
        body (CorrelateMessageData):

    Raises:
        errors.CorrelateMessageBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CorrelateMessageForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CorrelateMessageNotFound: If the response status code is 404. Not found
        errors.CorrelateMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CorrelateMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CorrelateMessageResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CorrelateMessageBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CorrelateMessageForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CorrelateMessageNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CorrelateMessageInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CorrelateMessageServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CorrelateMessageResponse200, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: CorrelateMessageData
) -> Response[
    CorrelateMessageResponse200
    | CorrelateMessageResponse400
    | CorrelateMessageResponse403
    | CorrelateMessageResponse404
    | CorrelateMessageResponse500
    | CorrelateMessageResponse503
]:
    """Correlate message

     Publishes a message and correlates it to a subscription.
    If correlation is successful it will return the first process instance key the message correlated
    with.
    The message is not buffered.
    Use the publish message endpoint to send messages that can be buffered.

    Args:
        body (CorrelateMessageData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorrelateMessageResponse200 | CorrelateMessageResponse400 | CorrelateMessageResponse403 | CorrelateMessageResponse404 | CorrelateMessageResponse500 | CorrelateMessageResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, body: CorrelateMessageData, **kwargs: Any
) -> CorrelateMessageResponse200:
    """Correlate message

     Publishes a message and correlates it to a subscription.
    If correlation is successful it will return the first process instance key the message correlated
    with.
    The message is not buffered.
    Use the publish message endpoint to send messages that can be buffered.

    Args:
        body (CorrelateMessageData):

    Raises:
        errors.CorrelateMessageBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CorrelateMessageForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CorrelateMessageNotFound: If the response status code is 404. Not found
        errors.CorrelateMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CorrelateMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CorrelateMessageResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CorrelateMessageBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CorrelateMessageForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CorrelateMessageNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CorrelateMessageInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CorrelateMessageServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CorrelateMessageResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CorrelateMessageResponse200, response.parsed)
