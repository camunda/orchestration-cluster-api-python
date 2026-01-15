from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assign_client_to_group_response_400 import AssignClientToGroupResponse400
from ...models.assign_client_to_group_response_403 import AssignClientToGroupResponse403
from ...models.assign_client_to_group_response_404 import AssignClientToGroupResponse404
from ...models.assign_client_to_group_response_409 import AssignClientToGroupResponse409
from ...models.assign_client_to_group_response_500 import AssignClientToGroupResponse500
from ...models.assign_client_to_group_response_503 import AssignClientToGroupResponse503
from ...types import Response

def _get_kwargs(group_id: str, client_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/groups/{group_id}/clients/{client_id}'.format(group_id=quote(str(group_id), safe=''), client_id=quote(str(client_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = AssignClientToGroupResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = AssignClientToGroupResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = AssignClientToGroupResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = AssignClientToGroupResponse409.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = AssignClientToGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = AssignClientToGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(group_id: str, client_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]:
    """Assign a client to a group

     Assigns a client to a group, making it a member of the group.
    Members of the group inherit the group authorizations, roles, and tenant assignments.

    Args:
        group_id (str):
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, client_id=client_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(group_id: str, client_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Assign a client to a group

 Assigns a client to a group, making it a member of the group.
Members of the group inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.AssignClientToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.AssignClientToGroupConflict: If the response status code is 409. The client with the given ID is already assigned to the group.
    errors.AssignClientToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(group_id=group_id, client_id=client_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignClientToGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.AssignClientToGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.AssignClientToGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.AssignClientToGroupConflict(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.AssignClientToGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.AssignClientToGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(group_id: str, client_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]:
    """Assign a client to a group

     Assigns a client to a group, making it a member of the group.
    Members of the group inherit the group authorizations, roles, and tenant assignments.

    Args:
        group_id (str):
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, client_id=client_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(group_id: str, client_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Assign a client to a group

 Assigns a client to a group, making it a member of the group.
Members of the group inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.AssignClientToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.AssignClientToGroupConflict: If the response status code is 409. The client with the given ID is already assigned to the group.
    errors.AssignClientToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(group_id=group_id, client_id=client_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignClientToGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.AssignClientToGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.AssignClientToGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.AssignClientToGroupConflict(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.AssignClientToGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.AssignClientToGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(AssignClientToGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed