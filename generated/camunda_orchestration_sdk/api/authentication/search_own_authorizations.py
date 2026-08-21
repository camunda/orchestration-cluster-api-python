from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.authorization_search_query import AuthorizationSearchQuery
from ...models.own_authorization_search_result import OwnAuthorizationSearchResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: AuthorizationSearchQuery | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/authentication/me/authorizations/search",
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OwnAuthorizationSearchResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = OwnAuthorizationSearchResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]:
    """Search own authorizations

     Search for the current authenticated principal's own authorization records — including
    authorizations granted directly to the user or client, as well as those granted via a group, role,
    or mapping rule the principal belongs to.

    Args:
        body (AuthorizationSearchQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OwnAuthorizationSearchResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> OwnAuthorizationSearchResult:
    """Search own authorizations

     Search for the current authenticated principal's own authorization records — including
    authorizations granted directly to the user or client, as well as those granted via a group, role,
    or mapping rule the principal belongs to.

    Args:
        body (AuthorizationSearchQuery | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        OwnAuthorizationSearchResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="search_own_authorizations",
        )
    assert response.parsed is not None
    return cast(OwnAuthorizationSearchResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: AuthorizationSearchQuery | Unset = UNSET
) -> Response[OwnAuthorizationSearchResult | ProblemDetail]:
    """Search own authorizations

     Search for the current authenticated principal's own authorization records — including
    authorizations granted directly to the user or client, as well as those granted via a group, role,
    or mapping rule the principal belongs to.

    Args:
        body (AuthorizationSearchQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OwnAuthorizationSearchResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthorizationSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> OwnAuthorizationSearchResult:
    """Search own authorizations

     Search for the current authenticated principal's own authorization records — including
    authorizations granted directly to the user or client, as well as those granted via a group, role,
    or mapping rule the principal belongs to.

    Args:
        body (AuthorizationSearchQuery | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        OwnAuthorizationSearchResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_own_authorizations",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="search_own_authorizations",
        )
    assert response.parsed is not None
    return cast(OwnAuthorizationSearchResult, response.parsed)
