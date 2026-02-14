from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_user_task_form_response_200 import GetUserTaskFormResponse200
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(user_task_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user-tasks/{user_task_key}/form".format(
            user_task_key=quote(str(user_task_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GetUserTaskFormResponse200 | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = GetUserTaskFormResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Any | GetUserTaskFormResponse200 | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | GetUserTaskFormResponse200 | ProblemDetail]:
    """Get user task form

     Get the form of a user task.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetUserTaskFormResponse200 | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetUserTaskFormResponse200:
    """Get user task form

     Get the form of a user task.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.GetUserTaskFormBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUserTaskFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUserTaskFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUserTaskFormNotFound: If the response status code is 404. Not found
        errors.GetUserTaskFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetUserTaskFormResponse200"""
    response = sync_detailed(user_task_key=user_task_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUserTaskFormBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUserTaskFormUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUserTaskFormForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetUserTaskFormNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUserTaskFormInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetUserTaskFormResponse200, response.parsed)


async def asyncio_detailed(
    user_task_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | GetUserTaskFormResponse200 | ProblemDetail]:
    """Get user task form

     Get the form of a user task.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetUserTaskFormResponse200 | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetUserTaskFormResponse200:
    """Get user task form

     Get the form of a user task.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        user_task_key (str): System-generated key for a user task.

    Raises:
        errors.GetUserTaskFormBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUserTaskFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUserTaskFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUserTaskFormNotFound: If the response status code is 404. Not found
        errors.GetUserTaskFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetUserTaskFormResponse200"""
    response = await asyncio_detailed(user_task_key=user_task_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUserTaskFormBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUserTaskFormUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUserTaskFormForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetUserTaskFormNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUserTaskFormInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetUserTaskFormResponse200, response.parsed)
