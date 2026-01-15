from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_tenant_response_200 import GetTenantResponse200
from ...models.get_tenant_response_400 import GetTenantResponse400
from ...models.get_tenant_response_401 import GetTenantResponse401
from ...models.get_tenant_response_403 import GetTenantResponse403
from ...models.get_tenant_response_404 import GetTenantResponse404
from ...models.get_tenant_response_500 import GetTenantResponse500
from ...types import Response

def _get_kwargs(tenant_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/tenants/{tenant_id}'.format(tenant_id=quote(str(tenant_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500 | None:
    if response.status_code == 200:
        response_200 = GetTenantResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetTenantResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetTenantResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetTenantResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetTenantResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetTenantResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(tenant_id: str, *, client: AuthenticatedClient | Client) -> Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetTenantResponse200:
    """Get tenant

 Retrieves a single tenant by tenant ID.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
    errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantResponse200"""
    response = sync_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetTenantBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetTenantUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetTenantForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetTenantNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetTenantInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(tenant_id: str, *, client: AuthenticatedClient | Client) -> Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetTenantResponse200:
    """Get tenant

 Retrieves a single tenant by tenant ID.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
    errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantResponse200"""
    response = await asyncio_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetTenantBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetTenantUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetTenantForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetTenantNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetTenantInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetTenantResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed