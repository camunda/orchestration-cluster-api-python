from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_statistics_by_error_data import GetProcessInstanceStatisticsByErrorData
from ...models.get_process_instance_statistics_by_error_response_200 import GetProcessInstanceStatisticsByErrorResponse200
from ...models.get_process_instance_statistics_by_error_response_400 import GetProcessInstanceStatisticsByErrorResponse400
from ...models.get_process_instance_statistics_by_error_response_401 import GetProcessInstanceStatisticsByErrorResponse401
from ...models.get_process_instance_statistics_by_error_response_403 import GetProcessInstanceStatisticsByErrorResponse403
from ...models.get_process_instance_statistics_by_error_response_500 import GetProcessInstanceStatisticsByErrorResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: GetProcessInstanceStatisticsByErrorData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/incidents/statistics/process-instances-by-error'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500 | None:
    if response.status_code == 200:
        response_200 = GetProcessInstanceStatisticsByErrorResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceStatisticsByErrorResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceStatisticsByErrorResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceStatisticsByErrorResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = GetProcessInstanceStatisticsByErrorResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByErrorData | Unset=UNSET) -> Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]:
    """Get process instance statistics by error

     Returns statistics for active process instances that currently have active incidents,
    grouped by incident error hash code.

    Args:
        body (GetProcessInstanceStatisticsByErrorData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByErrorData | Unset=UNSET, **kwargs: Any) -> GetProcessInstanceStatisticsByErrorResponse200:
    """Get process instance statistics by error

 Returns statistics for active process instances that currently have active incidents,
grouped by incident error hash code.

Args:
    body (GetProcessInstanceStatisticsByErrorData | Unset):

Raises:
    errors.GetProcessInstanceStatisticsByErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByErrorUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByErrorForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByErrorResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsByErrorBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsByErrorUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsByErrorForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsByErrorInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceStatisticsByErrorResponse200, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByErrorData | Unset=UNSET) -> Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]:
    """Get process instance statistics by error

     Returns statistics for active process instances that currently have active incidents,
    grouped by incident error hash code.

    Args:
        body (GetProcessInstanceStatisticsByErrorData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: GetProcessInstanceStatisticsByErrorData | Unset=UNSET, **kwargs: Any) -> GetProcessInstanceStatisticsByErrorResponse200:
    """Get process instance statistics by error

 Returns statistics for active process instances that currently have active incidents,
grouped by incident error hash code.

Args:
    body (GetProcessInstanceStatisticsByErrorData | Unset):

Raises:
    errors.GetProcessInstanceStatisticsByErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByErrorUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByErrorForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByErrorResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceStatisticsByErrorBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetProcessInstanceStatisticsByErrorUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetProcessInstanceStatisticsByErrorForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.GetProcessInstanceStatisticsByErrorInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetProcessInstanceStatisticsByErrorResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceStatisticsByErrorResponse200, response.parsed)