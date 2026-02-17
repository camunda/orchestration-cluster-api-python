from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_task_result import UserTaskResult
from ...types import Response


def _get_kwargs(user_task_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user-tasks/{user_task_key}".format(
            user_task_key=quote(str(user_task_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UserTaskResult | None:
    if response.status_code == 200:
        response_200 = UserTaskResult.from_dict(response.json())
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
) -> Response[ProblemDetail | UserTaskResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | UserTaskResult]:
    """Get user task

     Get the user task by the user task key.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserTaskResult]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> UserTaskResult:
    """Get user task

     Get the user task by the user task key.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.GetUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUserTaskUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUserTaskForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
        errors.GetUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserTaskResult"""
    response = sync_detailed(user_task_key=user_task_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUserTaskBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUserTaskUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUserTaskForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetUserTaskNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUserTaskInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UserTaskResult, response.parsed)


async def asyncio_detailed(
    user_task_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | UserTaskResult]:
    """Get user task

     Get the user task by the user task key.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserTaskResult]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> UserTaskResult:
    """Get user task

     Get the user task by the user task key.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.GetUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUserTaskUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUserTaskForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
        errors.GetUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserTaskResult"""
    response = await asyncio_detailed(user_task_key=user_task_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUserTaskBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUserTaskUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUserTaskForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetUserTaskNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUserTaskInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UserTaskResult, response.parsed)
