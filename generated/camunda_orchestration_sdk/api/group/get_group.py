from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_result import GroupResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(group_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/groups/{group_id}".format(group_id=quote(str(group_id), safe="")),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GroupResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = GroupResult.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GroupResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str, *, client: AuthenticatedClient | Client
) -> Response[GroupResult | ProblemDetail]:
    """Get group

     Get a group by its ID.

    Args:
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GroupResult | ProblemDetail]
    """
    kwargs = _get_kwargs(group_id=group_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GroupResult:
    """Get group

     Get a group by its ID.

    Args:
        group_id (str):

    Raises:
        errors.GetGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.GetGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GroupResult"""
    response = sync_detailed(group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GroupResult, response.parsed)


async def asyncio_detailed(
    group_id: str, *, client: AuthenticatedClient | Client
) -> Response[GroupResult | ProblemDetail]:
    """Get group

     Get a group by its ID.

    Args:
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GroupResult | ProblemDetail]
    """
    kwargs = _get_kwargs(group_id=group_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GroupResult:
    """Get group

     Get a group by its ID.

    Args:
        group_id (str):

    Raises:
        errors.GetGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.GetGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GroupResult"""
    response = await asyncio_detailed(group_id=group_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GroupResult, response.parsed)
