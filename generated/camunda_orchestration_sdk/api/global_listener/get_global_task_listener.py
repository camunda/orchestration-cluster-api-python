from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_task_listener_result import GlobalTaskListenerResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/global-task-listeners/{id}".format(id=quote(str(id), safe="")),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GlobalTaskListenerResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = GlobalTaskListenerResult.from_dict(response.json())
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
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str, *, client: AuthenticatedClient | Client
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    """Get global user task listener

     Get a global user task listener by its id.

    Args:
        id (str): The user-defined id for the global listener Example: GlobalListener_1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalTaskListenerResult | ProblemDetail]
    """
    kwargs = _get_kwargs(id=id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GlobalTaskListenerResult:
    """Get global user task listener

     Get a global user task listener by its id.

    Args:
        id (str): The user-defined id for the global listener Example: GlobalListener_1.

    Raises:
        errors.GetGlobalTaskListenerUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalTaskListenerForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalTaskListenerNotFound: If the response status code is 404. The global user task listener with the given id was not found.
        errors.GetGlobalTaskListenerInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalTaskListenerResult"""
    response = sync_detailed(id=id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetGlobalTaskListenerUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalTaskListenerForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGlobalTaskListenerNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalTaskListenerInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalTaskListenerResult, response.parsed)


async def asyncio_detailed(
    id: str, *, client: AuthenticatedClient | Client
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    """Get global user task listener

     Get a global user task listener by its id.

    Args:
        id (str): The user-defined id for the global listener Example: GlobalListener_1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalTaskListenerResult | ProblemDetail]
    """
    kwargs = _get_kwargs(id=id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GlobalTaskListenerResult:
    """Get global user task listener

     Get a global user task listener by its id.

    Args:
        id (str): The user-defined id for the global listener Example: GlobalListener_1.

    Raises:
        errors.GetGlobalTaskListenerUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalTaskListenerForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalTaskListenerNotFound: If the response status code is 404. The global user task listener with the given id was not found.
        errors.GetGlobalTaskListenerInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalTaskListenerResult"""
    response = await asyncio_detailed(id=id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetGlobalTaskListenerUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalTaskListenerForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGlobalTaskListenerNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalTaskListenerInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalTaskListenerResult, response.parsed)
