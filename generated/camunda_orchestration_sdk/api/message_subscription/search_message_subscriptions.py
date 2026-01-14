from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_message_subscriptions_data import SearchMessageSubscriptionsData
from ...models.search_message_subscriptions_response_200 import SearchMessageSubscriptionsResponse200
from ...models.search_message_subscriptions_response_400 import SearchMessageSubscriptionsResponse400
from ...models.search_message_subscriptions_response_401 import SearchMessageSubscriptionsResponse401
from ...models.search_message_subscriptions_response_403 import SearchMessageSubscriptionsResponse403
from ...models.search_message_subscriptions_response_500 import SearchMessageSubscriptionsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchMessageSubscriptionsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/message-subscriptions/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchMessageSubscriptionsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchMessageSubscriptionsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchMessageSubscriptionsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchMessageSubscriptionsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = SearchMessageSubscriptionsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchMessageSubscriptionsData | Unset=UNSET) -> Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]:
    """Search message subscriptions

     Search for message subscriptions based on given criteria.

    Args:
        body (SearchMessageSubscriptionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchMessageSubscriptionsData | Unset=UNSET, **kwargs) -> SearchMessageSubscriptionsResponse200:
    """Search message subscriptions

 Search for message subscriptions based on given criteria.

Args:
    body (SearchMessageSubscriptionsData | Unset):

Raises:
    errors.SearchMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMessageSubscriptionsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchMessageSubscriptionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchMessageSubscriptionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchMessageSubscriptionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchMessageSubscriptionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchMessageSubscriptionsData | Unset=UNSET) -> Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]:
    """Search message subscriptions

     Search for message subscriptions based on given criteria.

    Args:
        body (SearchMessageSubscriptionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchMessageSubscriptionsData | Unset=UNSET, **kwargs) -> SearchMessageSubscriptionsResponse200:
    """Search message subscriptions

 Search for message subscriptions based on given criteria.

Args:
    body (SearchMessageSubscriptionsData | Unset):

Raises:
    errors.SearchMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMessageSubscriptionsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchMessageSubscriptionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchMessageSubscriptionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchMessageSubscriptionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchMessageSubscriptionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchMessageSubscriptionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed