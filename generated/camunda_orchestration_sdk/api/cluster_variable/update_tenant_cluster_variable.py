from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_tenant_cluster_variable_data import UpdateTenantClusterVariableData
from ...models.update_tenant_cluster_variable_response_200 import UpdateTenantClusterVariableResponse200
from ...models.update_tenant_cluster_variable_response_400 import UpdateTenantClusterVariableResponse400
from ...models.update_tenant_cluster_variable_response_401 import UpdateTenantClusterVariableResponse401
from ...models.update_tenant_cluster_variable_response_403 import UpdateTenantClusterVariableResponse403
from ...models.update_tenant_cluster_variable_response_404 import UpdateTenantClusterVariableResponse404
from ...models.update_tenant_cluster_variable_response_500 import UpdateTenantClusterVariableResponse500
from ...types import Response

def _get_kwargs(tenant_id: str, name: str, *, body: UpdateTenantClusterVariableData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/cluster-variables/tenants/{tenant_id}/{name}'.format(tenant_id=quote(str(tenant_id), safe=''), name=quote(str(name), safe=''))}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500 | None:
    if response.status_code == 200:
        response_200 = UpdateTenantClusterVariableResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = UpdateTenantClusterVariableResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = UpdateTenantClusterVariableResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = UpdateTenantClusterVariableResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = UpdateTenantClusterVariableResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UpdateTenantClusterVariableResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(tenant_id: str, name: str, *, client: AuthenticatedClient | Client, body: UpdateTenantClusterVariableData) -> Response[UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500]:
    """Update a tenant-scoped cluster variable

     Updates the value of an existing tenant-scoped cluster variable.
    The variable must exist, otherwise a 404 error is returned.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):
        body (UpdateTenantClusterVariableData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, name=name, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(tenant_id: str, name: str, *, client: AuthenticatedClient | Client, body: UpdateTenantClusterVariableData, **kwargs) -> UpdateTenantClusterVariableResponse200:
    """Update a tenant-scoped cluster variable

 Updates the value of an existing tenant-scoped cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):
    body (UpdateTenantClusterVariableData):

Raises:
    errors.UpdateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantClusterVariableResponse200"""
    response = sync_detailed(tenant_id=tenant_id, name=name, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateTenantClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateTenantClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateTenantClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateTenantClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateTenantClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(tenant_id: str, name: str, *, client: AuthenticatedClient | Client, body: UpdateTenantClusterVariableData) -> Response[UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500]:
    """Update a tenant-scoped cluster variable

     Updates the value of an existing tenant-scoped cluster variable.
    The variable must exist, otherwise a 404 error is returned.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):
        body (UpdateTenantClusterVariableData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateTenantClusterVariableResponse200 | UpdateTenantClusterVariableResponse400 | UpdateTenantClusterVariableResponse401 | UpdateTenantClusterVariableResponse403 | UpdateTenantClusterVariableResponse404 | UpdateTenantClusterVariableResponse500]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, name=name, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(tenant_id: str, name: str, *, client: AuthenticatedClient | Client, body: UpdateTenantClusterVariableData, **kwargs) -> UpdateTenantClusterVariableResponse200:
    """Update a tenant-scoped cluster variable

 Updates the value of an existing tenant-scoped cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):
    body (UpdateTenantClusterVariableData):

Raises:
    errors.UpdateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantClusterVariableResponse200"""
    response = await asyncio_detailed(tenant_id=tenant_id, name=name, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateTenantClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateTenantClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateTenantClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateTenantClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateTenantClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateTenantClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed