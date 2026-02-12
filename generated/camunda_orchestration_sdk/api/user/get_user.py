from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_user_response_200 import GetUserResponse200
from ...models.get_user_response_401 import GetUserResponse401
from ...models.get_user_response_403 import GetUserResponse403
from ...models.get_user_response_404 import GetUserResponse404
from ...models.get_user_response_500 import GetUserResponse500
from ...types import Response

def _get_kwargs(username: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/users/{username}'.format(username=quote(str(username), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500 | None:
    if response.status_code == 200:
        response_200 = GetUserResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = GetUserResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetUserResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetUserResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetUserResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(username: str, *, client: AuthenticatedClient | Client) -> Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]:
    """Get user

     Get a user by its username.

    Args:
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]
    """
    kwargs = _get_kwargs(username=username)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(username: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> GetUserResponse200:
    """Get user

 Get a user by its username.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.GetUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserNotFound: If the response status code is 404. The user with the given username was not found.
    errors.GetUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserResponse200"""
    response = sync_detailed(username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetUserUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetUserResponse200, response.parsed)

async def asyncio_detailed(username: str, *, client: AuthenticatedClient | Client) -> Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]:
    """Get user

     Get a user by its username.

    Args:
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]
    """
    kwargs = _get_kwargs(username=username)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(username: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> GetUserResponse200:
    """Get user

 Get a user by its username.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.GetUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserNotFound: If the response status code is 404. The user with the given username was not found.
    errors.GetUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserResponse200"""
    response = await asyncio_detailed(username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetUserUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetUserResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetUserResponse200, response.parsed)