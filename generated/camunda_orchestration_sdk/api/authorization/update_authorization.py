from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.object_ import Object
from ...models.object_1 import Object1
from ...models.update_authorization_response_401 import UpdateAuthorizationResponse401
from ...models.update_authorization_response_404 import UpdateAuthorizationResponse404
from ...models.update_authorization_response_500 import UpdateAuthorizationResponse500
from ...models.update_authorization_response_503 import UpdateAuthorizationResponse503
from ...types import Response

def _get_kwargs(authorization_key: str, *, body: Object | Object1) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/authorizations/{authorization_key}'.format(authorization_key=quote(str(authorization_key), safe=''))}
    if isinstance(body, Object):
        _kwargs['json'] = body.to_dict()
    else:
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 401:
        response_401 = UpdateAuthorizationResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = UpdateAuthorizationResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UpdateAuthorizationResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = UpdateAuthorizationResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(authorization_key: str, *, client: AuthenticatedClient | Client, body: Object | Object1) -> Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]:
    """Update authorization

     Update the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.
        body (Object | Object1): Defines an authorization request.
            Either an id-based or a property-based authorization can be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(authorization_key: str, *, client: AuthenticatedClient | Client, body: Object | Object1, **kwargs) -> Any:
    """Update authorization

 Update the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.UpdateAuthorizationUnauthorized: If the response status code is 401.
    errors.UpdateAuthorizationNotFound: If the response status code is 404.
    errors.UpdateAuthorizationInternalServerError: If the response status code is 500.
    errors.UpdateAuthorizationServiceUnavailable: If the response status code is 503.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(authorization_key=authorization_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UpdateAuthorizationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateAuthorizationNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateAuthorizationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateAuthorizationServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(authorization_key: str, *, client: AuthenticatedClient | Client, body: Object | Object1) -> Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]:
    """Update authorization

     Update the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.
        body (Object | Object1): Defines an authorization request.
            Either an id-based or a property-based authorization can be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(authorization_key: str, *, client: AuthenticatedClient | Client, body: Object | Object1, **kwargs) -> Any:
    """Update authorization

 Update the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.UpdateAuthorizationUnauthorized: If the response status code is 401.
    errors.UpdateAuthorizationNotFound: If the response status code is 404.
    errors.UpdateAuthorizationInternalServerError: If the response status code is 500.
    errors.UpdateAuthorizationServiceUnavailable: If the response status code is 503.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(authorization_key=authorization_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UpdateAuthorizationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateAuthorizationNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateAuthorizationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateAuthorizationServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateAuthorizationResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed