from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.broadcast_signal_data import BroadcastSignalData
from ...models.broadcast_signal_response_200 import BroadcastSignalResponse200
from ...models.broadcast_signal_response_400 import BroadcastSignalResponse400
from ...models.broadcast_signal_response_404 import BroadcastSignalResponse404
from ...models.broadcast_signal_response_500 import BroadcastSignalResponse500
from ...models.broadcast_signal_response_503 import BroadcastSignalResponse503
from ...types import Response

def _get_kwargs(*, body: BroadcastSignalData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/signals/broadcast'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503 | None:
    if response.status_code == 200:
        response_200 = BroadcastSignalResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = BroadcastSignalResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = BroadcastSignalResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = BroadcastSignalResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = BroadcastSignalResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: BroadcastSignalData) -> Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]:
    """Broadcast signal

     Broadcasts a signal.

    Args:
        body (BroadcastSignalData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: BroadcastSignalData, **kwargs) -> BroadcastSignalResponse200:
    """Broadcast signal

 Broadcasts a signal.

Args:
    body (BroadcastSignalData):

Raises:
    errors.BroadcastSignalBadRequest: If the response status code is 400. The provided data is not valid.
    errors.BroadcastSignalNotFound: If the response status code is 404. The signal is not found.
    errors.BroadcastSignalInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.BroadcastSignalServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    BroadcastSignalResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BroadcastSignalBadRequest(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.BroadcastSignalNotFound(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.BroadcastSignalInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.BroadcastSignalServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: BroadcastSignalData) -> Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]:
    """Broadcast signal

     Broadcasts a signal.

    Args:
        body (BroadcastSignalData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: BroadcastSignalData, **kwargs) -> BroadcastSignalResponse200:
    """Broadcast signal

 Broadcasts a signal.

Args:
    body (BroadcastSignalData):

Raises:
    errors.BroadcastSignalBadRequest: If the response status code is 400. The provided data is not valid.
    errors.BroadcastSignalNotFound: If the response status code is 404. The signal is not found.
    errors.BroadcastSignalInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.BroadcastSignalServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    BroadcastSignalResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BroadcastSignalBadRequest(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.BroadcastSignalNotFound(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.BroadcastSignalInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.BroadcastSignalServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(BroadcastSignalResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed