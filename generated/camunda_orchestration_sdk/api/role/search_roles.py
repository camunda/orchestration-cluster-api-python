from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_roles_data import SearchRolesData
from ...models.search_roles_response_200 import SearchRolesResponse200
from ...models.search_roles_response_400 import SearchRolesResponse400
from ...models.search_roles_response_401 import SearchRolesResponse401
from ...models.search_roles_response_403 import SearchRolesResponse403
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchRolesData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/roles/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403 | None:
    if response.status_code == 200:
        response_200 = SearchRolesResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchRolesResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchRolesResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchRolesResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchRolesData | Unset=UNSET) -> Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]:
    """Search roles

     Search for roles based on given criteria.

    Args:
        body (SearchRolesData | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchRolesData | Unset=UNSET, **kwargs: Any) -> SearchRolesResponse200:
    """Search roles

 Search for roles based on given criteria.

Args:
    body (SearchRolesData | Unset): Role search request.

Raises:
    errors.SearchRolesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchRolesBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchRolesUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchRolesForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchRolesInternalServerError(status_code=response.status_code, content=response.content, parsed=response.parsed)
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchRolesResponse200, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchRolesData | Unset=UNSET) -> Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]:
    """Search roles

     Search for roles based on given criteria.

    Args:
        body (SearchRolesData | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchRolesData | Unset=UNSET, **kwargs: Any) -> SearchRolesResponse200:
    """Search roles

 Search for roles based on given criteria.

Args:
    body (SearchRolesData | Unset): Role search request.

Raises:
    errors.SearchRolesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchRolesBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchRolesUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchRolesForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchRolesResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchRolesInternalServerError(status_code=response.status_code, content=response.content, parsed=response.parsed)
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchRolesResponse200, response.parsed)