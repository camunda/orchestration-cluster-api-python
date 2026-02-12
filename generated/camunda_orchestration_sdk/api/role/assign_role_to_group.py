from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assign_role_to_group_response_400 import AssignRoleToGroupResponse400
from ...models.assign_role_to_group_response_403 import AssignRoleToGroupResponse403
from ...models.assign_role_to_group_response_404 import AssignRoleToGroupResponse404
from ...models.assign_role_to_group_response_409 import AssignRoleToGroupResponse409
from ...models.assign_role_to_group_response_500 import AssignRoleToGroupResponse500
from ...models.assign_role_to_group_response_503 import AssignRoleToGroupResponse503
from ...types import Response


def _get_kwargs(role_id: str, group_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/roles/{role_id}/groups/{group_id}".format(
            role_id=quote(str(role_id), safe=""), group_id=quote(str(group_id), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | AssignRoleToGroupResponse400
    | AssignRoleToGroupResponse403
    | AssignRoleToGroupResponse404
    | AssignRoleToGroupResponse409
    | AssignRoleToGroupResponse500
    | AssignRoleToGroupResponse503
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = AssignRoleToGroupResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = AssignRoleToGroupResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = AssignRoleToGroupResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = AssignRoleToGroupResponse409.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = AssignRoleToGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = AssignRoleToGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | AssignRoleToGroupResponse400
    | AssignRoleToGroupResponse403
    | AssignRoleToGroupResponse404
    | AssignRoleToGroupResponse409
    | AssignRoleToGroupResponse500
    | AssignRoleToGroupResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    role_id: str, group_id: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | AssignRoleToGroupResponse400
    | AssignRoleToGroupResponse403
    | AssignRoleToGroupResponse404
    | AssignRoleToGroupResponse409
    | AssignRoleToGroupResponse500
    | AssignRoleToGroupResponse503
]:
    """Assign a role to a group

     Assigns the specified role to the group. Every member of the group (user or client) will inherit the
    authorizations associated with this role.

    Args:
        role_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignRoleToGroupResponse400 | AssignRoleToGroupResponse403 | AssignRoleToGroupResponse404 | AssignRoleToGroupResponse409 | AssignRoleToGroupResponse500 | AssignRoleToGroupResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, group_id=group_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    role_id: str, group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Assign a role to a group

     Assigns the specified role to the group. Every member of the group (user or client) will inherit the
    authorizations associated with this role.

    Args:
        role_id (str):
        group_id (str):

    Raises:
        errors.AssignRoleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.AssignRoleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.AssignRoleToGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
        errors.AssignRoleToGroupConflict: If the response status code is 409. The role is already assigned to the group with the given ID.
        errors.AssignRoleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.AssignRoleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(role_id=role_id, group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignRoleToGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.AssignRoleToGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.AssignRoleToGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse404, response.parsed),
            )
        if response.status_code == 409:
            raise errors.AssignRoleToGroupConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse409, response.parsed),
            )
        if response.status_code == 500:
            raise errors.AssignRoleToGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.AssignRoleToGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    role_id: str, group_id: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | AssignRoleToGroupResponse400
    | AssignRoleToGroupResponse403
    | AssignRoleToGroupResponse404
    | AssignRoleToGroupResponse409
    | AssignRoleToGroupResponse500
    | AssignRoleToGroupResponse503
]:
    """Assign a role to a group

     Assigns the specified role to the group. Every member of the group (user or client) will inherit the
    authorizations associated with this role.

    Args:
        role_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignRoleToGroupResponse400 | AssignRoleToGroupResponse403 | AssignRoleToGroupResponse404 | AssignRoleToGroupResponse409 | AssignRoleToGroupResponse500 | AssignRoleToGroupResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, group_id=group_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    role_id: str, group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Assign a role to a group

     Assigns the specified role to the group. Every member of the group (user or client) will inherit the
    authorizations associated with this role.

    Args:
        role_id (str):
        group_id (str):

    Raises:
        errors.AssignRoleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.AssignRoleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.AssignRoleToGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
        errors.AssignRoleToGroupConflict: If the response status code is 409. The role is already assigned to the group with the given ID.
        errors.AssignRoleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.AssignRoleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(role_id=role_id, group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignRoleToGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse400, response.parsed),
            )
        if response.status_code == 403:
            raise errors.AssignRoleToGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.AssignRoleToGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse404, response.parsed),
            )
        if response.status_code == 409:
            raise errors.AssignRoleToGroupConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse409, response.parsed),
            )
        if response.status_code == 500:
            raise errors.AssignRoleToGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.AssignRoleToGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(AssignRoleToGroupResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
