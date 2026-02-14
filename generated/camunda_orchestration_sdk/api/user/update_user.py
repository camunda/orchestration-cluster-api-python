from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_result import UserResult
from ...models.user_update_request import UserUpdateRequest
from ...types import Response


def _get_kwargs(username: str, *, body: UserUpdateRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/users/{username}".format(username=quote(str(username), safe="")),
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UserResult | None:
    if response.status_code == 200:
        response_200 = UserResult.from_dict(response.json())
        return response_200
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
) -> Response[ProblemDetail | UserResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    username: str, *, client: AuthenticatedClient | Client, body: UserUpdateRequest
) -> Response[ProblemDetail | UserResult]:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UserUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserResult]
    """
    kwargs = _get_kwargs(username=username, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserUpdateRequest,
    **kwargs: Any,
) -> UserResult:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UserUpdateRequest):

    Raises:
        errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
        errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserResult"""
    response = sync_detailed(username=username, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateUserBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UpdateUserForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UpdateUserNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UpdateUserInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UpdateUserServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UserResult, response.parsed)


async def asyncio_detailed(
    username: str, *, client: AuthenticatedClient | Client, body: UserUpdateRequest
) -> Response[ProblemDetail | UserResult]:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UserUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserResult]
    """
    kwargs = _get_kwargs(username=username, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    username: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserUpdateRequest,
    **kwargs: Any,
) -> UserResult:
    """Update user

     Updates a user.

    Args:
        username (str): The unique name of a user. Example: swillis.
        body (UserUpdateRequest):

    Raises:
        errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
        errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserResult"""
    response = await asyncio_detailed(username=username, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateUserBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UpdateUserForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UpdateUserNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UpdateUserInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UpdateUserServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UserResult, response.parsed)
