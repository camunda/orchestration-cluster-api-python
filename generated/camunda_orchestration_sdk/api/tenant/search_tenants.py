from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_tenants_data import SearchTenantsData
from ...models.search_tenants_response_200 import SearchTenantsResponse200
from ...models.search_tenants_response_400 import SearchTenantsResponse400
from ...models.search_tenants_response_401 import SearchTenantsResponse401
from ...models.search_tenants_response_403 import SearchTenantsResponse403
from ...models.search_tenants_response_500 import SearchTenantsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchTenantsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/tenants/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchTenantsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchTenantsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchTenantsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchTenantsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 500:
        response_500 = SearchTenantsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchTenantsData | Unset=UNSET) -> Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]:
    """Search tenants

     Retrieves a filtered and sorted list of tenants.

    Args:
        body (SearchTenantsData | Unset): Tenant search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchTenantsData | Unset=UNSET, **kwargs) -> Any:
    """Search tenants

 Retrieves a filtered and sorted list of tenants.

Args:
    body (SearchTenantsData | Unset): Tenant search request

Raises:
    errors.SearchTenantsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchTenantsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchTenantsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchTenantsNotFound: If the response status code is 404. Not found
    errors.SearchTenantsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchTenantsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchTenantsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchTenantsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.SearchTenantsNotFound(status_code=response.status_code, content=response.content, parsed=response.parsed)
        if response.status_code == 500:
            raise errors.SearchTenantsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchTenantsData | Unset=UNSET) -> Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]:
    """Search tenants

     Retrieves a filtered and sorted list of tenants.

    Args:
        body (SearchTenantsData | Unset): Tenant search request

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchTenantsData | Unset=UNSET, **kwargs) -> Any:
    """Search tenants

 Retrieves a filtered and sorted list of tenants.

Args:
    body (SearchTenantsData | Unset): Tenant search request

Raises:
    errors.SearchTenantsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchTenantsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchTenantsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchTenantsNotFound: If the response status code is 404. Not found
    errors.SearchTenantsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchTenantsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchTenantsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchTenantsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.SearchTenantsNotFound(status_code=response.status_code, content=response.content, parsed=response.parsed)
        if response.status_code == 500:
            raise errors.SearchTenantsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchTenantsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed