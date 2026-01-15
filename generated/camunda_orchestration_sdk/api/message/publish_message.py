from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.publish_message_data import PublishMessageData
from ...models.publish_message_response_200 import PublishMessageResponse200
from ...models.publish_message_response_400 import PublishMessageResponse400
from ...models.publish_message_response_500 import PublishMessageResponse500
from ...models.publish_message_response_503 import PublishMessageResponse503
from ...types import Response

def _get_kwargs(*, body: PublishMessageData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/messages/publication'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503 | None:
    if response.status_code == 200:
        response_200 = PublishMessageResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = PublishMessageResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 500:
        response_500 = PublishMessageResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = PublishMessageResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: PublishMessageData) -> Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]:
    """Publish message

     Publishes a single message.
    Messages are published to specific partitions computed from their correlation keys.
    Messages can be buffered.
    The endpoint does not wait for a correlation result.
    Use the message correlation endpoint for such use cases.

    Args:
        body (PublishMessageData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: PublishMessageData, **kwargs) -> PublishMessageResponse200:
    """Publish message

 Publishes a single message.
Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

Args:
    body (PublishMessageData):

Raises:
    errors.PublishMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PublishMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PublishMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    PublishMessageResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.PublishMessageBadRequest(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse400, response.parsed))
        if response.status_code == 500:
            raise errors.PublishMessageInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.PublishMessageServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: PublishMessageData) -> Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]:
    """Publish message

     Publishes a single message.
    Messages are published to specific partitions computed from their correlation keys.
    Messages can be buffered.
    The endpoint does not wait for a correlation result.
    Use the message correlation endpoint for such use cases.

    Args:
        body (PublishMessageData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: PublishMessageData, **kwargs) -> PublishMessageResponse200:
    """Publish message

 Publishes a single message.
Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

Args:
    body (PublishMessageData):

Raises:
    errors.PublishMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PublishMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PublishMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    PublishMessageResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.PublishMessageBadRequest(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse400, response.parsed))
        if response.status_code == 500:
            raise errors.PublishMessageInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.PublishMessageServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(PublishMessageResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed