from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activate_jobs_data import ActivateJobsData
from ...models.activate_jobs_response_200 import ActivateJobsResponse200
from ...models.activate_jobs_response_400 import ActivateJobsResponse400
from ...models.activate_jobs_response_401 import ActivateJobsResponse401
from ...models.activate_jobs_response_500 import ActivateJobsResponse500
from ...models.activate_jobs_response_503 import ActivateJobsResponse503
from ...types import Response

def _get_kwargs(*, body: ActivateJobsData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/jobs/activation'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503 | None:
    if response.status_code == 200:
        response_200 = ActivateJobsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ActivateJobsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ActivateJobsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 500:
        response_500 = ActivateJobsResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ActivateJobsResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: ActivateJobsData) -> Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]:
    """Activate jobs

     Iterate through all known partitions and activate jobs up to the requested maximum.

    Args:
        body (ActivateJobsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: ActivateJobsData, **kwargs) -> ActivateJobsResponse200:
    """Activate jobs

 Iterate through all known partitions and activate jobs up to the requested maximum.

Args:
    body (ActivateJobsData):

Raises:
    errors.ActivateJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateJobsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ActivateJobsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ActivateJobsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.ActivateJobsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse401, response.parsed))
        if response.status_code == 500:
            raise errors.ActivateJobsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.ActivateJobsServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: ActivateJobsData) -> Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]:
    """Activate jobs

     Iterate through all known partitions and activate jobs up to the requested maximum.

    Args:
        body (ActivateJobsData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: ActivateJobsData, **kwargs) -> ActivateJobsResponse200:
    """Activate jobs

 Iterate through all known partitions and activate jobs up to the requested maximum.

Args:
    body (ActivateJobsData):

Raises:
    errors.ActivateJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateJobsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ActivateJobsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ActivateJobsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.ActivateJobsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse401, response.parsed))
        if response.status_code == 500:
            raise errors.ActivateJobsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.ActivateJobsServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(ActivateJobsResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed