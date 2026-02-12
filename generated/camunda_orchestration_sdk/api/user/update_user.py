from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_user_data import UpdateUserData
from ...models.update_user_response_200 import UpdateUserResponse200
from ...models.update_user_response_400 import UpdateUserResponse400
from ...models.update_user_response_403 import UpdateUserResponse403
from ...models.update_user_response_404 import UpdateUserResponse404
from ...models.update_user_response_500 import UpdateUserResponse500
from ...models.update_user_response_503 import UpdateUserResponse503
from ...types import Response

def _get_kwargs(username: str, *, body: UpdateUserData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/users/{username}'.format(username=quote(str(username), safe=''))}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503 | None:
    if response.status_code == 200:
        response_200 = UpdateUserResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = UpdateUserResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = UpdateUserResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = UpdateUserResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UpdateUserResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = UpdateUserResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(username: str, *, client: AuthenticatedClient | Client, body: UpdateUserData) -> Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UpdateUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]
    """
    kwargs = _get_kwargs(username=username, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(username: str, *, client: AuthenticatedClient | Client, body: UpdateUserData, **kwargs: Any) -> UpdateUserResponse200:
    """Update user

 Updates a user.

Args:
    username (str): The unique name of a user. Example: swillis.
    body (UpdateUserData):

Raises:
    errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
    errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateUserResponse200"""
    response = sync_detailed(username=username, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UpdateUserResponse200, response.parsed)

async def asyncio_detailed(username: str, *, client: AuthenticatedClient | Client, body: UpdateUserData) -> Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UpdateUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]
    """
    kwargs = _get_kwargs(username=username, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(username: str, *, client: AuthenticatedClient | Client, body: UpdateUserData, **kwargs: Any) -> UpdateUserResponse200:
    """Update user

 Updates a user.

Args:
    username (str): The unique name of a user. Example: swillis.
    body (UpdateUserData):

Raises:
    errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
    errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateUserResponse200"""
    response = await asyncio_detailed(username=username, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateUserNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UpdateUserResponse200, response.parsed)