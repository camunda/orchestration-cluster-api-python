from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_admin_user_data import CreateAdminUserData
from ...models.create_admin_user_response_400 import CreateAdminUserResponse400
from ...models.create_admin_user_response_403 import CreateAdminUserResponse403
from ...models.create_admin_user_response_500 import CreateAdminUserResponse500
from ...models.create_admin_user_response_503 import CreateAdminUserResponse503
from ...types import Response

def _get_kwargs(*, body: CreateAdminUserData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/setup/user'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503 | None:
    if response.status_code == 201:
        response_201 = cast(Any, None)
        return response_201
    if response.status_code == 400:
        response_400 = CreateAdminUserResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = CreateAdminUserResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = CreateAdminUserResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CreateAdminUserResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: CreateAdminUserData) -> Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]:
    """Create admin user

     Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
    managed in the Orchestration Cluster and while no user is assigned to the admin role.

    Args:
        body (CreateAdminUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: CreateAdminUserData, **kwargs) -> Any:
    """Create admin user

 Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
managed in the Orchestration Cluster and while no user is assigned to the admin role.

Args:
    body (CreateAdminUserData):

Raises:
    errors.CreateAdminUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAdminUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAdminUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAdminUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateAdminUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.CreateAdminUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.CreateAdminUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CreateAdminUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: CreateAdminUserData) -> Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]:
    """Create admin user

     Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
    managed in the Orchestration Cluster and while no user is assigned to the admin role.

    Args:
        body (CreateAdminUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: CreateAdminUserData, **kwargs) -> Any:
    """Create admin user

 Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
managed in the Orchestration Cluster and while no user is assigned to the admin role.

Args:
    body (CreateAdminUserData):

Raises:
    errors.CreateAdminUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAdminUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAdminUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAdminUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateAdminUserBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.CreateAdminUserForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.CreateAdminUserInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CreateAdminUserServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CreateAdminUserResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed