from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_statistics_by_definition_data import GetProcessInstanceStatisticsByDefinitionData
from ...models.get_process_instance_statistics_by_definition_response_200 import GetProcessInstanceStatisticsByDefinitionResponse200
from ...models.get_process_instance_statistics_by_definition_response_400 import GetProcessInstanceStatisticsByDefinitionResponse400
from ...models.get_process_instance_statistics_by_definition_response_401 import GetProcessInstanceStatisticsByDefinitionResponse401
from ...models.get_process_instance_statistics_by_definition_response_403 import GetProcessInstanceStatisticsByDefinitionResponse403
from ...models.get_process_instance_statistics_by_definition_response_500 import GetProcessInstanceStatisticsByDefinitionResponse500
from ...types import Response

def _get_kwargs(*, body: GetProcessInstanceStatisticsByDefinitionData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/incidents/statistics/process-instances-by-definition'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500 | None:
    if response.status_code == 200:
        response_200 = GetProcessInstanceStatisticsByDefinitionResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceStatisticsByDefinitionResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceStatisticsByDefinitionResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceStatisticsByDefinitionResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = GetProcessInstanceStatisticsByDefinitionResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByDefinitionData) -> Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]:
    """Get process instance statistics by definition

     Returns statistics for active process instances with incidents, grouped by process
    definition. The result set is scoped to a specific incident error hash code, which must be
    provided as a filter in the request body.

    Args:
        body (GetProcessInstanceStatisticsByDefinitionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByDefinitionData, **kwargs) -> GetProcessInstanceStatisticsByDefinitionResponse200:
    """Get process instance statistics by definition

 Returns statistics for active process instances with incidents, grouped by process
definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

Args:
    body (GetProcessInstanceStatisticsByDefinitionData):

Raises:
    errors.GetProcessInstanceStatisticsByDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByDefinitionResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsByDefinitionBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsByDefinitionUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsByDefinitionForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsByDefinitionInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByDefinitionData) -> Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]:
    """Get process instance statistics by definition

     Returns statistics for active process instances with incidents, grouped by process
    definition. The result set is scoped to a specific incident error hash code, which must be
    provided as a filter in the request body.

    Args:
        body (GetProcessInstanceStatisticsByDefinitionData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByDefinitionData, **kwargs) -> GetProcessInstanceStatisticsByDefinitionResponse200:
    """Get process instance statistics by definition

 Returns statistics for active process instances with incidents, grouped by process
definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

Args:
    body (GetProcessInstanceStatisticsByDefinitionData):

Raises:
    errors.GetProcessInstanceStatisticsByDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByDefinitionResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsByDefinitionBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsByDefinitionUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsByDefinitionForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsByDefinitionInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByDefinitionResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed