from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_clients_for_group_data import SearchClientsForGroupData
from ...models.tenant_client_search_result import TenantClientSearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: str, *, body: SearchClientsForGroupData | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/groups/{group_id}/clients/search".format(
            group_id=quote(str(group_id), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantClientSearchResult | None:
    if response.status_code == 200:
        response_200 = TenantClientSearchResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
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
) -> Response[ProblemDetail | TenantClientSearchResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchClientsForGroupData | Unset = UNSET,
) -> Response[ProblemDetail | TenantClientSearchResult]:
    """Search group clients

     Search clients assigned to a group.

    Args:
        group_id (str):
        body (SearchClientsForGroupData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantClientSearchResult]
    """
    kwargs = _get_kwargs(group_id=group_id, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchClientsForGroupData | Unset = UNSET,
    **kwargs: Any,
) -> TenantClientSearchResult:
    """Search group clients

     Search clients assigned to a group.

    Args:
        group_id (str):
        body (SearchClientsForGroupData | Unset):

    Raises:
        errors.SearchClientsForGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchClientsForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchClientsForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchClientsForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.SearchClientsForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantClientSearchResult"""
    response = sync_detailed(group_id=group_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClientsForGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchClientsForGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchClientsForGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchClientsForGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchClientsForGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantClientSearchResult, response.parsed)


async def asyncio_detailed(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchClientsForGroupData | Unset = UNSET,
) -> Response[ProblemDetail | TenantClientSearchResult]:
    """Search group clients

     Search clients assigned to a group.

    Args:
        group_id (str):
        body (SearchClientsForGroupData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantClientSearchResult]
    """
    kwargs = _get_kwargs(group_id=group_id, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchClientsForGroupData | Unset = UNSET,
    **kwargs: Any,
) -> TenantClientSearchResult:
    """Search group clients

     Search clients assigned to a group.

    Args:
        group_id (str):
        body (SearchClientsForGroupData | Unset):

    Raises:
        errors.SearchClientsForGroupBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchClientsForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchClientsForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchClientsForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
        errors.SearchClientsForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantClientSearchResult"""
    response = await asyncio_detailed(group_id=group_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClientsForGroupBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchClientsForGroupUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchClientsForGroupForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchClientsForGroupNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchClientsForGroupInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantClientSearchResult, response.parsed)
