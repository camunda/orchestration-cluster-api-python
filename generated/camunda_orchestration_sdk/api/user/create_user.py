from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_user_data import CreateUserData
from ...models.create_user_response_201 import CreateUserResponse201
from ...models.create_user_response_400 import CreateUserResponse400
from ...models.create_user_response_401 import CreateUserResponse401
from ...models.create_user_response_403 import CreateUserResponse403
from ...models.create_user_response_409 import CreateUserResponse409
from ...models.create_user_response_500 import CreateUserResponse500
from ...models.create_user_response_503 import CreateUserResponse503
from ...types import Response


def _get_kwargs(*, body: CreateUserData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/users"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateUserResponse201
    | CreateUserResponse400
    | CreateUserResponse401
    | CreateUserResponse403
    | CreateUserResponse409
    | CreateUserResponse500
    | CreateUserResponse503
    | None
):
    if response.status_code == 201:
        response_201 = CreateUserResponse201.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = CreateUserResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = CreateUserResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = CreateUserResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 409:
        response_409 = CreateUserResponse409.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = CreateUserResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CreateUserResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateUserResponse201
    | CreateUserResponse400
    | CreateUserResponse401
    | CreateUserResponse403
    | CreateUserResponse409
    | CreateUserResponse500
    | CreateUserResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: CreateUserData
) -> Response[
    CreateUserResponse201
    | CreateUserResponse400
    | CreateUserResponse401
    | CreateUserResponse403
    | CreateUserResponse409
    | CreateUserResponse500
    | CreateUserResponse503
]:
    """Create user

     Create a new user.

    Args:
        body (CreateUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateUserResponse201 | CreateUserResponse400 | CreateUserResponse401 | CreateUserResponse403 | CreateUserResponse409 | CreateUserResponse500 | CreateUserResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, body: CreateUserData, **kwargs: Any
) -> CreateUserResponse201:
    """Create user

     Create a new user.

    Args:
        body (CreateUserData):

    Raises:
        errors.CreateUserBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateUserConflict: If the response status code is 409. A user with this username already exists.
        errors.CreateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateUserResponse201"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateUserBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateUserUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateUserForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse403, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateUserConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse409, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateUserInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateUserServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateUserResponse201, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: CreateUserData
) -> Response[
    CreateUserResponse201
    | CreateUserResponse400
    | CreateUserResponse401
    | CreateUserResponse403
    | CreateUserResponse409
    | CreateUserResponse500
    | CreateUserResponse503
]:
    """Create user

     Create a new user.

    Args:
        body (CreateUserData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateUserResponse201 | CreateUserResponse400 | CreateUserResponse401 | CreateUserResponse403 | CreateUserResponse409 | CreateUserResponse500 | CreateUserResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, body: CreateUserData, **kwargs: Any
) -> CreateUserResponse201:
    """Create user

     Create a new user.

    Args:
        body (CreateUserData):

    Raises:
        errors.CreateUserBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateUserConflict: If the response status code is 409. A user with this username already exists.
        errors.CreateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateUserResponse201"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateUserBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateUserUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateUserForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse403, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateUserConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse409, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateUserInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateUserServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateUserResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateUserResponse201, response.parsed)
