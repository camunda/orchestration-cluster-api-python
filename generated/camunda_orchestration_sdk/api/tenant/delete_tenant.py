from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_tenant_response_400 import DeleteTenantResponse400
from ...models.delete_tenant_response_403 import DeleteTenantResponse403
from ...models.delete_tenant_response_404 import DeleteTenantResponse404
from ...models.delete_tenant_response_500 import DeleteTenantResponse500
from ...models.delete_tenant_response_503 import DeleteTenantResponse503
from ...types import Response

def _get_kwargs(tenant_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'delete', 'url': '/tenants/{tenant_id}'.format(tenant_id=quote(str(tenant_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = DeleteTenantResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = DeleteTenantResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = DeleteTenantResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = DeleteTenantResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = DeleteTenantResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(tenant_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]:
    """Delete tenant

     Deletes an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Delete tenant

 Deletes an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.DeleteTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.DeleteTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteTenantBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.DeleteTenantForbidden(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteTenantNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteTenantInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteTenantServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(tenant_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]:
    """Delete tenant

     Deletes an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Delete tenant

 Deletes an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.DeleteTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.DeleteTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteTenantBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.DeleteTenantForbidden(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteTenantNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteTenantInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteTenantServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteTenantResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed