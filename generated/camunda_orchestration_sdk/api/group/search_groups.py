from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_groups_data import SearchGroupsData
from ...models.search_groups_response_200 import SearchGroupsResponse200
from ...models.search_groups_response_400 import SearchGroupsResponse400
from ...models.search_groups_response_401 import SearchGroupsResponse401
from ...models.search_groups_response_403 import SearchGroupsResponse403
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: SearchGroupsData | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/groups/search"}
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | SearchGroupsResponse200
    | SearchGroupsResponse400
    | SearchGroupsResponse401
    | SearchGroupsResponse403
    | None
):
    if response.status_code == 200:
        response_200 = SearchGroupsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchGroupsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchGroupsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchGroupsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | SearchGroupsResponse200
    | SearchGroupsResponse400
    | SearchGroupsResponse401
    | SearchGroupsResponse403
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: SearchGroupsData | Unset = UNSET
) -> Response[
    Any
    | SearchGroupsResponse200
    | SearchGroupsResponse400
    | SearchGroupsResponse401
    | SearchGroupsResponse403
]:
    """Search groups

     Search for groups based on given criteria.

    Args:
        body (SearchGroupsData | Unset): Group search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchGroupsResponse200 | SearchGroupsResponse400 | SearchGroupsResponse401 | SearchGroupsResponse403]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: SearchGroupsData | Unset = UNSET,
    **kwargs: Any,
) -> SearchGroupsResponse200:
    """Search groups

     Search for groups based on given criteria.

    Args:
        body (SearchGroupsData | Unset): Group search request.

    Raises:
        errors.SearchGroupsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchGroupsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchGroupsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchGroupsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchGroupsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchGroupsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchGroupsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchGroupsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse403, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchGroupsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchGroupsResponse200, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: SearchGroupsData | Unset = UNSET
) -> Response[
    Any
    | SearchGroupsResponse200
    | SearchGroupsResponse400
    | SearchGroupsResponse401
    | SearchGroupsResponse403
]:
    """Search groups

     Search for groups based on given criteria.

    Args:
        body (SearchGroupsData | Unset): Group search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SearchGroupsResponse200 | SearchGroupsResponse400 | SearchGroupsResponse401 | SearchGroupsResponse403]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SearchGroupsData | Unset = UNSET,
    **kwargs: Any,
) -> SearchGroupsResponse200:
    """Search groups

     Search for groups based on given criteria.

    Args:
        body (SearchGroupsData | Unset): Group search request.

    Raises:
        errors.SearchGroupsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchGroupsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchGroupsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchGroupsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchGroupsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchGroupsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchGroupsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchGroupsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(SearchGroupsResponse403, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchGroupsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchGroupsResponse200, response.parsed)
