from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_group_data import UpdateGroupData
from ...models.update_group_response_200 import UpdateGroupResponse200
from ...models.update_group_response_400 import UpdateGroupResponse400
from ...models.update_group_response_401 import UpdateGroupResponse401
from ...models.update_group_response_404 import UpdateGroupResponse404
from ...models.update_group_response_500 import UpdateGroupResponse500
from ...models.update_group_response_503 import UpdateGroupResponse503
from ...types import Response

def _get_kwargs(group_id: str, *, body: UpdateGroupData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/groups/{group_id}'.format(group_id=quote(str(group_id), safe=''))}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503 | None:
    if response.status_code == 200:
        response_200 = UpdateGroupResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = UpdateGroupResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = UpdateGroupResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = UpdateGroupResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UpdateGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = UpdateGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(group_id: str, *, client: AuthenticatedClient | Client, body: UpdateGroupData) -> Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]:
    """Update group

     Update a group with the given ID.

    Args:
        group_id (str):
        body (UpdateGroupData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(group_id: str, *, client: AuthenticatedClient | Client, body: UpdateGroupData, **kwargs) -> UpdateGroupResponse200:
    """Update group

 Update a group with the given ID.

Args:
    group_id (str):
    body (UpdateGroupData):

Raises:
    errors.UpdateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.UpdateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGroupResponse200"""
    response = sync_detailed(group_id=group_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateGroupUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(group_id: str, *, client: AuthenticatedClient | Client, body: UpdateGroupData) -> Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]:
    """Update group

     Update a group with the given ID.

    Args:
        group_id (str):
        body (UpdateGroupData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(group_id: str, *, client: AuthenticatedClient | Client, body: UpdateGroupData, **kwargs) -> UpdateGroupResponse200:
    """Update group

 Update a group with the given ID.

Args:
    group_id (str):
    body (UpdateGroupData):

Raises:
    errors.UpdateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.UpdateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGroupResponse200"""
    response = await asyncio_detailed(group_id=group_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.UpdateGroupUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.UpdateGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UpdateGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UpdateGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UpdateGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed