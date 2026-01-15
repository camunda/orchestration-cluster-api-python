from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_authorizations_data import SearchAuthorizationsData
from ...models.search_authorizations_response_200 import SearchAuthorizationsResponse200
from ...models.search_authorizations_response_400 import SearchAuthorizationsResponse400
from ...models.search_authorizations_response_401 import SearchAuthorizationsResponse401
from ...models.search_authorizations_response_403 import SearchAuthorizationsResponse403
from ...models.search_authorizations_response_500 import SearchAuthorizationsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchAuthorizationsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/authorizations/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchAuthorizationsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchAuthorizationsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchAuthorizationsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchAuthorizationsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = SearchAuthorizationsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchAuthorizationsData | Unset=UNSET) -> Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]:
    """Search authorizations

     Search for authorizations based on given criteria.

    Args:
        body (SearchAuthorizationsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchAuthorizationsData | Unset=UNSET, **kwargs) -> SearchAuthorizationsResponse200:
    """Search authorizations

 Search for authorizations based on given criteria.

Args:
    body (SearchAuthorizationsData | Unset):

Raises:
    errors.SearchAuthorizationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuthorizationsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuthorizationsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuthorizationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuthorizationsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchAuthorizationsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchAuthorizationsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchAuthorizationsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchAuthorizationsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchAuthorizationsData | Unset=UNSET) -> Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]:
    """Search authorizations

     Search for authorizations based on given criteria.

    Args:
        body (SearchAuthorizationsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchAuthorizationsData | Unset=UNSET, **kwargs) -> SearchAuthorizationsResponse200:
    """Search authorizations

 Search for authorizations based on given criteria.

Args:
    body (SearchAuthorizationsData | Unset):

Raises:
    errors.SearchAuthorizationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuthorizationsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuthorizationsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuthorizationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuthorizationsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchAuthorizationsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchAuthorizationsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchAuthorizationsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchAuthorizationsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchAuthorizationsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed