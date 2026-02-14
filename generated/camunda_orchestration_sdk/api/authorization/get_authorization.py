from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.authorization_result import AuthorizationResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(authorization_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/authorizations/{authorization_key}".format(
            authorization_key=quote(str(authorization_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuthorizationResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = AuthorizationResult.from_dict(response.json())
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
) -> Response[AuthorizationResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    authorization_key: str, *, client: AuthenticatedClient | Client
) -> Response[AuthorizationResult | ProblemDetail]:
    """Get authorization

     Get authorization by the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthorizationResult | ProblemDetail]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    authorization_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> AuthorizationResult:
    """Get authorization

     Get authorization by the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.GetAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuthorizationNotFound: If the response status code is 404. The authorization with the given key was not found.
        errors.GetAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuthorizationResult"""
    response = sync_detailed(authorization_key=authorization_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthorizationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuthorizationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetAuthorizationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuthorizationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuthorizationResult, response.parsed)


async def asyncio_detailed(
    authorization_key: str, *, client: AuthenticatedClient | Client
) -> Response[AuthorizationResult | ProblemDetail]:
    """Get authorization

     Get authorization by the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthorizationResult | ProblemDetail]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    authorization_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> AuthorizationResult:
    """Get authorization

     Get authorization by the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.GetAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuthorizationNotFound: If the response status code is 404. The authorization with the given key was not found.
        errors.GetAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuthorizationResult"""
    response = await asyncio_detailed(
        authorization_key=authorization_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthorizationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuthorizationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetAuthorizationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuthorizationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuthorizationResult, response.parsed)
