from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_call_hierarchy_response_200_item import GetProcessInstanceCallHierarchyResponse200Item
from ...models.get_process_instance_call_hierarchy_response_400 import GetProcessInstanceCallHierarchyResponse400
from ...models.get_process_instance_call_hierarchy_response_401 import GetProcessInstanceCallHierarchyResponse401
from ...models.get_process_instance_call_hierarchy_response_403 import GetProcessInstanceCallHierarchyResponse403
from ...models.get_process_instance_call_hierarchy_response_404 import GetProcessInstanceCallHierarchyResponse404
from ...models.get_process_instance_call_hierarchy_response_500 import GetProcessInstanceCallHierarchyResponse500
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/process-instances/{process_instance_key}/call-hierarchy'.format(process_instance_key=quote(str(process_instance_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetProcessInstanceCallHierarchyResponse200Item.from_dict(response_200_item_data)
            response_200.append(response_200_item)
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceCallHierarchyResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceCallHierarchyResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceCallHierarchyResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetProcessInstanceCallHierarchyResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetProcessInstanceCallHierarchyResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetProcessInstanceCallHierarchyResponse400:
    """Get call hierarchy

 Returns the call hierarchy for a given process instance, showing its ancestry up to the root
instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400.
    errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401.
    errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403.
    errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404.
    errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceCallHierarchyResponse400"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceCallHierarchyBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceCallHierarchyUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceCallHierarchyForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetProcessInstanceCallHierarchyNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceCallHierarchyInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetProcessInstanceCallHierarchyResponse400:
    """Get call hierarchy

 Returns the call hierarchy for a given process instance, showing its ancestry up to the root
instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400.
    errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401.
    errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403.
    errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404.
    errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceCallHierarchyResponse400"""
    response = await asyncio_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceCallHierarchyBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceCallHierarchyUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceCallHierarchyForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetProcessInstanceCallHierarchyNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceCallHierarchyInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceCallHierarchyResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed