from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_correlated_message_subscriptions_data import SearchCorrelatedMessageSubscriptionsData
from ...models.search_correlated_message_subscriptions_response_200 import SearchCorrelatedMessageSubscriptionsResponse200
from ...models.search_correlated_message_subscriptions_response_400 import SearchCorrelatedMessageSubscriptionsResponse400
from ...models.search_correlated_message_subscriptions_response_401 import SearchCorrelatedMessageSubscriptionsResponse401
from ...models.search_correlated_message_subscriptions_response_403 import SearchCorrelatedMessageSubscriptionsResponse403
from ...models.search_correlated_message_subscriptions_response_500 import SearchCorrelatedMessageSubscriptionsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchCorrelatedMessageSubscriptionsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/correlated-message-subscriptions/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchCorrelatedMessageSubscriptionsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchCorrelatedMessageSubscriptionsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchCorrelatedMessageSubscriptionsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchCorrelatedMessageSubscriptionsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = SearchCorrelatedMessageSubscriptionsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchCorrelatedMessageSubscriptionsData | Unset=UNSET) -> Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (SearchCorrelatedMessageSubscriptionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchCorrelatedMessageSubscriptionsData | Unset=UNSET, **kwargs: Any) -> SearchCorrelatedMessageSubscriptionsResponse200:
    """Search correlated message subscriptions

 Search correlated message subscriptions based on given criteria.

Args:
    body (SearchCorrelatedMessageSubscriptionsData | Unset):

Raises:
    errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchCorrelatedMessageSubscriptionsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchCorrelatedMessageSubscriptionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchCorrelatedMessageSubscriptionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchCorrelatedMessageSubscriptionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchCorrelatedMessageSubscriptionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchCorrelatedMessageSubscriptionsResponse200, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchCorrelatedMessageSubscriptionsData | Unset=UNSET) -> Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (SearchCorrelatedMessageSubscriptionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchCorrelatedMessageSubscriptionsData | Unset=UNSET, **kwargs: Any) -> SearchCorrelatedMessageSubscriptionsResponse200:
    """Search correlated message subscriptions

 Search correlated message subscriptions based on given criteria.

Args:
    body (SearchCorrelatedMessageSubscriptionsData | Unset):

Raises:
    errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchCorrelatedMessageSubscriptionsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchCorrelatedMessageSubscriptionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchCorrelatedMessageSubscriptionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchCorrelatedMessageSubscriptionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchCorrelatedMessageSubscriptionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchCorrelatedMessageSubscriptionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchCorrelatedMessageSubscriptionsResponse200, response.parsed)