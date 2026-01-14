from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.unassign_role_from_user_response_400 import UnassignRoleFromUserResponse400
from ...models.unassign_role_from_user_response_403 import UnassignRoleFromUserResponse403
from ...models.unassign_role_from_user_response_404 import UnassignRoleFromUserResponse404
from ...models.unassign_role_from_user_response_500 import UnassignRoleFromUserResponse500
from ...models.unassign_role_from_user_response_503 import UnassignRoleFromUserResponse503
from ...types import Response

def _get_kwargs(role_id: str, username: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'delete', 'url': '/roles/{role_id}/users/{username}'.format(role_id=quote(str(role_id), safe=''), username=quote(str(username), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = UnassignRoleFromUserResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = UnassignRoleFromUserResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = UnassignRoleFromUserResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UnassignRoleFromUserResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = UnassignRoleFromUserResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(role_id: str, username: str, *, client: AuthenticatedClient | Client) -> Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]:
    """Unassign a role from a user

     Unassigns a role from a user. The user will no longer inherit the authorizations associated with
    this role.

    Args:
        role_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, username=username)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(role_id: str, username: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Unassign a role from a user

 Unassigns a role from a user. The user will no longer inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignRoleFromUserBadRequest: If the response status code is 400.
    errors.UnassignRoleFromUserForbidden: If the response status code is 403.
    errors.UnassignRoleFromUserNotFound: If the response status code is 404.
    errors.UnassignRoleFromUserInternalServerError: If the response status code is 500.
    errors.UnassignRoleFromUserServiceUnavailable: If the response status code is 503.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(role_id=role_id, username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignRoleFromUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UnassignRoleFromUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UnassignRoleFromUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UnassignRoleFromUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UnassignRoleFromUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(role_id: str, username: str, *, client: AuthenticatedClient | Client) -> Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]:
    """Unassign a role from a user

     Unassigns a role from a user. The user will no longer inherit the authorizations associated with
    this role.

    Args:
        role_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, username=username)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(role_id: str, username: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Unassign a role from a user

 Unassigns a role from a user. The user will no longer inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignRoleFromUserBadRequest: If the response status code is 400.
    errors.UnassignRoleFromUserForbidden: If the response status code is 403.
    errors.UnassignRoleFromUserNotFound: If the response status code is 404.
    errors.UnassignRoleFromUserInternalServerError: If the response status code is 500.
    errors.UnassignRoleFromUserServiceUnavailable: If the response status code is 503.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(role_id=role_id, username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignRoleFromUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UnassignRoleFromUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UnassignRoleFromUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UnassignRoleFromUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UnassignRoleFromUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed