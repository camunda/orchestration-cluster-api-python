from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_role_data import CreateRoleData
from ...models.create_role_response_201 import CreateRoleResponse201
from ...models.create_role_response_400 import CreateRoleResponse400
from ...models.create_role_response_401 import CreateRoleResponse401
from ...models.create_role_response_403 import CreateRoleResponse403
from ...models.create_role_response_500 import CreateRoleResponse500
from ...models.create_role_response_503 import CreateRoleResponse503
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: CreateRoleData | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/roles"}
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateRoleResponse201
    | CreateRoleResponse400
    | CreateRoleResponse401
    | CreateRoleResponse403
    | CreateRoleResponse500
    | CreateRoleResponse503
    | None
):
    if response.status_code == 201:
        response_201 = CreateRoleResponse201.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = CreateRoleResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = CreateRoleResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = CreateRoleResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = CreateRoleResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CreateRoleResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateRoleResponse201
    | CreateRoleResponse400
    | CreateRoleResponse401
    | CreateRoleResponse403
    | CreateRoleResponse500
    | CreateRoleResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: CreateRoleData | Unset = UNSET
) -> Response[
    CreateRoleResponse201
    | CreateRoleResponse400
    | CreateRoleResponse401
    | CreateRoleResponse403
    | CreateRoleResponse500
    | CreateRoleResponse503
]:
    """Create role

     Create a new role.

    Args:
        body (CreateRoleData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateRoleResponse201 | CreateRoleResponse400 | CreateRoleResponse401 | CreateRoleResponse403 | CreateRoleResponse500 | CreateRoleResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateRoleData | Unset = UNSET,
    **kwargs: Any,
) -> CreateRoleResponse201:
    """Create role

     Create a new role.

    Args:
        body (CreateRoleData | Unset):

    Raises:
        errors.CreateRoleBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateRoleResponse201"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateRoleBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateRoleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateRoleForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse403, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateRoleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateRoleServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateRoleResponse201, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: CreateRoleData | Unset = UNSET
) -> Response[
    CreateRoleResponse201
    | CreateRoleResponse400
    | CreateRoleResponse401
    | CreateRoleResponse403
    | CreateRoleResponse500
    | CreateRoleResponse503
]:
    """Create role

     Create a new role.

    Args:
        body (CreateRoleData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateRoleResponse201 | CreateRoleResponse400 | CreateRoleResponse401 | CreateRoleResponse403 | CreateRoleResponse500 | CreateRoleResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateRoleData | Unset = UNSET,
    **kwargs: Any,
) -> CreateRoleResponse201:
    """Create role

     Create a new role.

    Args:
        body (CreateRoleData | Unset):

    Raises:
        errors.CreateRoleBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateRoleResponse201"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateRoleBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateRoleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateRoleForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse403, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateRoleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateRoleServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateRoleResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateRoleResponse201, response.parsed)
