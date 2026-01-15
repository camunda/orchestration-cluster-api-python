from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_cluster_variables_data import SearchClusterVariablesData
from ...models.search_cluster_variables_response_200 import SearchClusterVariablesResponse200
from ...models.search_cluster_variables_response_400 import SearchClusterVariablesResponse400
from ...models.search_cluster_variables_response_401 import SearchClusterVariablesResponse401
from ...models.search_cluster_variables_response_403 import SearchClusterVariablesResponse403
from ...models.search_cluster_variables_response_500 import SearchClusterVariablesResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchClusterVariablesData | Unset=UNSET, truncate_values: bool | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params['truncateValues'] = truncate_values
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/cluster-variables/search', 'params': params}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchClusterVariablesResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchClusterVariablesResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchClusterVariablesResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchClusterVariablesResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = SearchClusterVariablesResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchClusterVariablesData | Unset=UNSET, truncate_values: bool | Unset=UNSET) -> Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchClusterVariablesData | Unset): Cluster variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchClusterVariablesData | Unset=UNSET, truncate_values: bool | Unset=UNSET, **kwargs) -> SearchClusterVariablesResponse200:
    """Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchClusterVariablesData | Unset): Cluster variable search query request.

Raises:
    errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClusterVariablesResponse200"""
    response = sync_detailed(client=client, body=body, truncate_values=truncate_values)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClusterVariablesBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchClusterVariablesUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchClusterVariablesForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchClusterVariablesInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchClusterVariablesData | Unset=UNSET, truncate_values: bool | Unset=UNSET) -> Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchClusterVariablesData | Unset): Cluster variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchClusterVariablesData | Unset=UNSET, truncate_values: bool | Unset=UNSET, **kwargs) -> SearchClusterVariablesResponse200:
    """Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchClusterVariablesData | Unset): Cluster variable search query request.

Raises:
    errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClusterVariablesResponse200"""
    response = await asyncio_detailed(client=client, body=body, truncate_values=truncate_values)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClusterVariablesBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchClusterVariablesUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchClusterVariablesForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchClusterVariablesInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchClusterVariablesResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed