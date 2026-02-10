from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_global_cluster_variable_data import UpdateGlobalClusterVariableData
from ...models.update_global_cluster_variable_response_200 import UpdateGlobalClusterVariableResponse200
from ...models.update_global_cluster_variable_response_400 import UpdateGlobalClusterVariableResponse400
from ...models.update_global_cluster_variable_response_401 import UpdateGlobalClusterVariableResponse401
from ...models.update_global_cluster_variable_response_403 import UpdateGlobalClusterVariableResponse403
from ...models.update_global_cluster_variable_response_404 import UpdateGlobalClusterVariableResponse404
from ...models.update_global_cluster_variable_response_500 import UpdateGlobalClusterVariableResponse500
from ...types import Response

def _get_kwargs(name: str, *, body: UpdateGlobalClusterVariableData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/cluster-variables/global/{name}'.format(name=quote(str(name), safe=''))}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500 | None:
    if response.status_code == 200:
        response_200 = UpdateGlobalClusterVariableResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = UpdateGlobalClusterVariableResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = UpdateGlobalClusterVariableResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = UpdateGlobalClusterVariableResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = UpdateGlobalClusterVariableResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UpdateGlobalClusterVariableResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(name: str, *, client: AuthenticatedClient | Client, body: UpdateGlobalClusterVariableData) -> Response[UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500]:
    """Update a global-scoped cluster variable

     Updates the value of an existing global cluster variable.
    The variable must exist, otherwise a 404 error is returned.

    Args:
        name (str):
        body (UpdateGlobalClusterVariableData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500]
    """
    kwargs = _get_kwargs(name=name, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(name: str, *, client: AuthenticatedClient | Client, body: UpdateGlobalClusterVariableData, **kwargs) -> UpdateGlobalClusterVariableResponse200:
    """Update a global-scoped cluster variable

 Updates the value of an existing global cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    name (str):
    body (UpdateGlobalClusterVariableData):

Raises:
    errors.UpdateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGlobalClusterVariableResponse200"""
    response = sync_detailed(name=name, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateGlobalClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateGlobalClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateGlobalClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateGlobalClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateGlobalClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(name: str, *, client: AuthenticatedClient | Client, body: UpdateGlobalClusterVariableData) -> Response[UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500]:
    """Update a global-scoped cluster variable

     Updates the value of an existing global cluster variable.
    The variable must exist, otherwise a 404 error is returned.

    Args:
        name (str):
        body (UpdateGlobalClusterVariableData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGlobalClusterVariableResponse200 | UpdateGlobalClusterVariableResponse400 | UpdateGlobalClusterVariableResponse401 | UpdateGlobalClusterVariableResponse403 | UpdateGlobalClusterVariableResponse404 | UpdateGlobalClusterVariableResponse500]
    """
    kwargs = _get_kwargs(name=name, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(name: str, *, client: AuthenticatedClient | Client, body: UpdateGlobalClusterVariableData, **kwargs) -> UpdateGlobalClusterVariableResponse200:
    """Update a global-scoped cluster variable

 Updates the value of an existing global cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    name (str):
    body (UpdateGlobalClusterVariableData):

Raises:
    errors.UpdateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGlobalClusterVariableResponse200"""
    response = await asyncio_detailed(name=name, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateGlobalClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateGlobalClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.UpdateGlobalClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateGlobalClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateGlobalClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateGlobalClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed