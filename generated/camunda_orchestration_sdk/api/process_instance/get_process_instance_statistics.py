from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_statistics_response_200 import GetProcessInstanceStatisticsResponse200
from ...models.get_process_instance_statistics_response_400 import GetProcessInstanceStatisticsResponse400
from ...models.get_process_instance_statistics_response_401 import GetProcessInstanceStatisticsResponse401
from ...models.get_process_instance_statistics_response_403 import GetProcessInstanceStatisticsResponse403
from ...models.get_process_instance_statistics_response_500 import GetProcessInstanceStatisticsResponse500
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/process-instances/{process_instance_key}/statistics/element-instances'.format(process_instance_key=quote(str(process_instance_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500 | None:
    if response.status_code == 200:
        response_200 = GetProcessInstanceStatisticsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceStatisticsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceStatisticsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceStatisticsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = GetProcessInstanceStatisticsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]:
    """Get element instance statistics

     Get statistics about elements by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> GetProcessInstanceStatisticsResponse200:
    """Get element instance statistics

 Get statistics about elements by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsResponse200"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceStatisticsResponse200, response.parsed)

async def asyncio_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]:
    """Get element instance statistics

     Get statistics about elements by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> GetProcessInstanceStatisticsResponse200:
    """Get element instance statistics

 Get statistics about elements by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsResponse200"""
    response = await asyncio_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceStatisticsResponse200, response.parsed)