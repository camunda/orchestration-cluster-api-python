from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(group_id: str, username: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/groups/{group_id}/users/{username}".format(
            group_id=quote(str(group_id), safe=""),
            username=quote(str(username), safe=""),
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str, username: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Unassign a user from a group

     Unassigns a user from a group.
    The user is removed as a group member, with associated authorizations, roles, and tenant assignments
    no longer applied.

    Args:
        group_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(group_id=group_id, username=username)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    group_id: str, username: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Unassign a user from a group

     Unassigns a user from a group.
    The user is removed as a group member, with associated authorizations, roles, and tenant assignments
    no longer applied.

    Args:
        group_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnassignUserFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UnassignUserFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UnassignUserFromGroupNotFound: If the response status code is 404. The group or user with the given ID was not found, or the user is not assigned to this group.
        errors.UnassignUserFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnassignUserFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(group_id=group_id, username=username, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignUserFromGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UnassignUserFromGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UnassignUserFromGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UnassignUserFromGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UnassignUserFromGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    group_id: str, username: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Unassign a user from a group

     Unassigns a user from a group.
    The user is removed as a group member, with associated authorizations, roles, and tenant assignments
    no longer applied.

    Args:
        group_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(group_id=group_id, username=username)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str, username: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Unassign a user from a group

     Unassigns a user from a group.
    The user is removed as a group member, with associated authorizations, roles, and tenant assignments
    no longer applied.

    Args:
        group_id (str):
        username (str): The unique name of a user. Example: swillis.

    Raises:
        errors.UnassignUserFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UnassignUserFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UnassignUserFromGroupNotFound: If the response status code is 404. The group or user with the given ID was not found, or the user is not assigned to this group.
        errors.UnassignUserFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnassignUserFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        group_id=group_id, username=username, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignUserFromGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UnassignUserFromGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UnassignUserFromGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UnassignUserFromGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UnassignUserFromGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
