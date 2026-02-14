from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.camunda_user_result import CamundaUserResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/authentication/me"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CamundaUserResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = CamundaUserResult.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CamundaUserResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[CamundaUserResult | ProblemDetail]:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CamundaUserResult | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient, **kwargs: Any) -> CamundaUserResult:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CamundaUserResult"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthenticationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuthenticationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuthenticationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CamundaUserResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[CamundaUserResult | ProblemDetail]:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CamundaUserResult | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(*, client: AuthenticatedClient, **kwargs: Any) -> CamundaUserResult:
    """Get current user

     Retrieves the current authenticated user.

    Raises:
        errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CamundaUserResult"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuthenticationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuthenticationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuthenticationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CamundaUserResult, response.parsed)
