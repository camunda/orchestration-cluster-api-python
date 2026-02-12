from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resolve_process_instance_incidents_response_200 import ResolveProcessInstanceIncidentsResponse200
from ...models.resolve_process_instance_incidents_response_400 import ResolveProcessInstanceIncidentsResponse400
from ...models.resolve_process_instance_incidents_response_401 import ResolveProcessInstanceIncidentsResponse401
from ...models.resolve_process_instance_incidents_response_404 import ResolveProcessInstanceIncidentsResponse404
from ...models.resolve_process_instance_incidents_response_500 import ResolveProcessInstanceIncidentsResponse500
from ...models.resolve_process_instance_incidents_response_503 import ResolveProcessInstanceIncidentsResponse503
from ...types import Response

def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/process-instances/{process_instance_key}/incident-resolution'.format(process_instance_key=quote(str(process_instance_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503 | None:
    if response.status_code == 200:
        response_200 = ResolveProcessInstanceIncidentsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ResolveProcessInstanceIncidentsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ResolveProcessInstanceIncidentsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = ResolveProcessInstanceIncidentsResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ResolveProcessInstanceIncidentsResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ResolveProcessInstanceIncidentsResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]:
    """Resolve related incidents

     Creates a batch operation to resolve multiple incidents of a process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> ResolveProcessInstanceIncidentsResponse200:
    """Resolve related incidents

 Creates a batch operation to resolve multiple incidents of a process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.ResolveProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance is not found.
    errors.ResolveProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveProcessInstanceIncidentsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveProcessInstanceIncidentsResponse200"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ResolveProcessInstanceIncidentsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.ResolveProcessInstanceIncidentsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.ResolveProcessInstanceIncidentsNotFound(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.ResolveProcessInstanceIncidentsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.ResolveProcessInstanceIncidentsServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ResolveProcessInstanceIncidentsResponse200, response.parsed)

async def asyncio_detailed(process_instance_key: str, *, client: AuthenticatedClient | Client) -> Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]:
    """Resolve related incidents

     Creates a batch operation to resolve multiple incidents of a process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> ResolveProcessInstanceIncidentsResponse200:
    """Resolve related incidents

 Creates a batch operation to resolve multiple incidents of a process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.ResolveProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance is not found.
    errors.ResolveProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveProcessInstanceIncidentsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveProcessInstanceIncidentsResponse200"""
    response = await asyncio_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ResolveProcessInstanceIncidentsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.ResolveProcessInstanceIncidentsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.ResolveProcessInstanceIncidentsNotFound(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.ResolveProcessInstanceIncidentsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.ResolveProcessInstanceIncidentsServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(ResolveProcessInstanceIncidentsResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ResolveProcessInstanceIncidentsResponse200, response.parsed)