from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_sequence_flows_response_200 import GetProcessInstanceSequenceFlowsResponse200
from ...models.get_process_instance_sequence_flows_response_400 import GetProcessInstanceSequenceFlowsResponse400
from ...models.get_process_instance_sequence_flows_response_401 import GetProcessInstanceSequenceFlowsResponse401
from ...models.get_process_instance_sequence_flows_response_403 import GetProcessInstanceSequenceFlowsResponse403
from ...models.get_process_instance_sequence_flows_response_500 import GetProcessInstanceSequenceFlowsResponse500
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/process-instances/{process_instance_key}/sequence-flows'.format(process_instance_key=quote(str(process_instance_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500 | None:
    if response.status_code == 200:
        response_200 = GetProcessInstanceSequenceFlowsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceSequenceFlowsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceSequenceFlowsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceSequenceFlowsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = GetProcessInstanceSequenceFlowsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetProcessInstanceSequenceFlowsResponse200:
    """Get sequence flows

 Get sequence flows taken by the process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400.
    errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401.
    errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403.
    errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceSequenceFlowsResponse200"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceSequenceFlowsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceSequenceFlowsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceSequenceFlowsForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceSequenceFlowsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetProcessInstanceSequenceFlowsResponse200:
    """Get sequence flows

 Get sequence flows taken by the process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400.
    errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401.
    errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403.
    errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceSequenceFlowsResponse200"""
    response = await asyncio_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceSequenceFlowsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceSequenceFlowsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceSequenceFlowsForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceSequenceFlowsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceSequenceFlowsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed