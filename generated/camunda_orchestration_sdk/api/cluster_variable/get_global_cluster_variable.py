from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_global_cluster_variable_response_200 import GetGlobalClusterVariableResponse200
from ...models.get_global_cluster_variable_response_400 import GetGlobalClusterVariableResponse400
from ...models.get_global_cluster_variable_response_401 import GetGlobalClusterVariableResponse401
from ...models.get_global_cluster_variable_response_403 import GetGlobalClusterVariableResponse403
from ...models.get_global_cluster_variable_response_404 import GetGlobalClusterVariableResponse404
from ...models.get_global_cluster_variable_response_500 import GetGlobalClusterVariableResponse500
from ...types import Response

def _get_kwargs(name: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/cluster-variables/global/{name}'.format(name=quote(str(name), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500 | None:
    if response.status_code == 200:
        response_200 = GetGlobalClusterVariableResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetGlobalClusterVariableResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetGlobalClusterVariableResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetGlobalClusterVariableResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetGlobalClusterVariableResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetGlobalClusterVariableResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(name: str, *, client: AuthenticatedClient | Client) -> Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]:
    """Get a global-scoped cluster variable

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]
    """
    kwargs = _get_kwargs(name=name)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(name: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetGlobalClusterVariableResponse200:
    """Get a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalClusterVariableResponse200"""
    response = sync_detailed(name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetGlobalClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetGlobalClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetGlobalClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetGlobalClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(name: str, *, client: AuthenticatedClient | Client) -> Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]:
    """Get a global-scoped cluster variable

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]
    """
    kwargs = _get_kwargs(name=name)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(name: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetGlobalClusterVariableResponse200:
    """Get a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalClusterVariableResponse200"""
    response = await asyncio_detailed(name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalClusterVariableBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetGlobalClusterVariableUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetGlobalClusterVariableForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetGlobalClusterVariableNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetGlobalClusterVariableInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetGlobalClusterVariableResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed