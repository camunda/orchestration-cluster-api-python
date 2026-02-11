from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_group_response_401 import DeleteGroupResponse401
from ...models.delete_group_response_404 import DeleteGroupResponse404
from ...models.delete_group_response_500 import DeleteGroupResponse500
from ...models.delete_group_response_503 import DeleteGroupResponse503
from ...types import Response


def _get_kwargs(group_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/groups/{group_id}".format(group_id=quote(str(group_id), safe="")),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | DeleteGroupResponse401
    | DeleteGroupResponse404
    | DeleteGroupResponse500
    | DeleteGroupResponse503
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 401:
        response_401 = DeleteGroupResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = DeleteGroupResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = DeleteGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = DeleteGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | DeleteGroupResponse401
    | DeleteGroupResponse404
    | DeleteGroupResponse500
    | DeleteGroupResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | DeleteGroupResponse401
    | DeleteGroupResponse404
    | DeleteGroupResponse500
    | DeleteGroupResponse503
]:
    """Delete group

     Deletes the group with the given ID.

    Args:
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteGroupResponse401 | DeleteGroupResponse404 | DeleteGroupResponse500 | DeleteGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> None:
    """Delete group

     Deletes the group with the given ID.

    Args:
        group_id (str):

    Raises:
        errors.DeleteGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.DeleteGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse401, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    group_id: str, *, client: AuthenticatedClient | Client
) -> Response[
    Any
    | DeleteGroupResponse401
    | DeleteGroupResponse404
    | DeleteGroupResponse500
    | DeleteGroupResponse503
]:
    """Delete group

     Deletes the group with the given ID.

    Args:
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteGroupResponse401 | DeleteGroupResponse404 | DeleteGroupResponse500 | DeleteGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Delete group

     Deletes the group with the given ID.

    Args:
        group_id (str):

    Raises:
        errors.DeleteGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.DeleteGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse401, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteGroupServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(DeleteGroupResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
