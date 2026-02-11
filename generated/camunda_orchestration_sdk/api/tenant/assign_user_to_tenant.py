from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assign_user_to_tenant_response_400 import AssignUserToTenantResponse400
from ...models.assign_user_to_tenant_response_403 import AssignUserToTenantResponse403
from ...models.assign_user_to_tenant_response_404 import AssignUserToTenantResponse404
from ...models.assign_user_to_tenant_response_500 import AssignUserToTenantResponse500
from ...models.assign_user_to_tenant_response_503 import AssignUserToTenantResponse503
from ...types import Response


def _get_kwargs(tenant_id: str, username: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/tenants/{tenant_id}/users/{username}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            username=quote(str(username), safe=""),
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | AssignUserToTenantResponse400
    | AssignUserToTenantResponse403
    | AssignUserToTenantResponse404
    | AssignUserToTenantResponse500
    | AssignUserToTenantResponse503
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = AssignUserToTenantResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = AssignUserToTenantResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = AssignUserToTenantResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = AssignUserToTenantResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = AssignUserToTenantResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | AssignUserToTenantResponse400
    | AssignUserToTenantResponse403
    | AssignUserToTenantResponse404
    | AssignUserToTenantResponse500
    | AssignUserToTenantResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str, username: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | AssignUserToTenantResponse400
    | AssignUserToTenantResponse403
    | AssignUserToTenantResponse404
    | AssignUserToTenantResponse500
    | AssignUserToTenantResponse503
]:
    """Assign a user to a tenant

     Assign a single user to a specified tenant. The user can then access tenant data and perform
    authorized actions.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignUserToTenantResponse400 | AssignUserToTenantResponse403 | AssignUserToTenantResponse404 | AssignUserToTenantResponse500 | AssignUserToTenantResponse503]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, username=username)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> None:
    """Assign a user to a tenant

     Assign a single user to a specified tenant. The user can then access tenant data and perform
    authorized actions.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.AssignUserToTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.AssignUserToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.AssignUserToTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
        errors.AssignUserToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.AssignUserToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(tenant_id=tenant_id, username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignUserToTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.AssignUserToTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.AssignUserToTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.AssignUserToTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.AssignUserToTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    tenant_id: str, username: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | AssignUserToTenantResponse400
    | AssignUserToTenantResponse403
    | AssignUserToTenantResponse404
    | AssignUserToTenantResponse500
    | AssignUserToTenantResponse503
]:
    """Assign a user to a tenant

     Assign a single user to a specified tenant. The user can then access tenant data and perform
    authorized actions.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignUserToTenantResponse400 | AssignUserToTenantResponse403 | AssignUserToTenantResponse404 | AssignUserToTenantResponse500 | AssignUserToTenantResponse503]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, username=username)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    username: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> None:
    """Assign a user to a tenant

     Assign a single user to a specified tenant. The user can then access tenant data and perform
    authorized actions.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.AssignUserToTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.AssignUserToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.AssignUserToTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
        errors.AssignUserToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.AssignUserToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        tenant_id=tenant_id, username=username, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignUserToTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.AssignUserToTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.AssignUserToTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.AssignUserToTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.AssignUserToTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignUserToTenantResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
