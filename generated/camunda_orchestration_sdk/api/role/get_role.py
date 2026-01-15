from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_role_response_200 import GetRoleResponse200
from ...models.get_role_response_401 import GetRoleResponse401
from ...models.get_role_response_403 import GetRoleResponse403
from ...models.get_role_response_404 import GetRoleResponse404
from ...models.get_role_response_500 import GetRoleResponse500
from ...types import Response

def _get_kwargs(role_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/roles/{role_id}'.format(role_id=quote(str(role_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500 | None:
    if response.status_code == 200:
        response_200 = GetRoleResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = GetRoleResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetRoleResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetRoleResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetRoleResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(role_id: str, *, client: AuthenticatedClient | Client) -> Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]:
    """Get role

     Get a role by its ID.

    Args:
        role_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]
    """
    kwargs = _get_kwargs(role_id=role_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(role_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetRoleResponse200:
    """Get role

 Get a role by its ID.

Args:
    role_id (str):

Raises:
    errors.GetRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.GetRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetRoleResponse200"""
    response = sync_detailed(role_id=role_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetRoleUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetRoleForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetRoleNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetRoleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(role_id: str, *, client: AuthenticatedClient | Client) -> Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]:
    """Get role

     Get a role by its ID.

    Args:
        role_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]
    """
    kwargs = _get_kwargs(role_id=role_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(role_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetRoleResponse200:
    """Get role

 Get a role by its ID.

Args:
    role_id (str):

Raises:
    errors.GetRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.GetRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetRoleResponse200"""
    response = await asyncio_detailed(role_id=role_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetRoleUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetRoleForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetRoleNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetRoleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetRoleResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed