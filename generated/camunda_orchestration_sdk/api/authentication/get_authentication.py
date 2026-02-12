from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_authentication_response_200 import GetAuthenticationResponse200
from ...models.get_authentication_response_401 import GetAuthenticationResponse401
from ...models.get_authentication_response_403 import GetAuthenticationResponse403
from ...models.get_authentication_response_500 import GetAuthenticationResponse500
from ...types import Response

def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/authentication/me'}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500 | None:
    if response.status_code == 200:
        response_200 = GetAuthenticationResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = GetAuthenticationResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetAuthenticationResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = GetAuthenticationResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient) -> Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient, **kwargs: Any) -> GetAuthenticationResponse200:
    """Get current user

 Retrieves the current authenticated user.

Raises:
    errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthenticationResponse200"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthenticationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetAuthenticationForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetAuthenticationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetAuthenticationResponse200, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient) -> Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient, **kwargs: Any) -> GetAuthenticationResponse200:
    """Get current user

 Retrieves the current authenticated user.

Raises:
    errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthenticationResponse200"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthenticationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetAuthenticationForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetAuthenticationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetAuthenticationResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetAuthenticationResponse200, response.parsed)