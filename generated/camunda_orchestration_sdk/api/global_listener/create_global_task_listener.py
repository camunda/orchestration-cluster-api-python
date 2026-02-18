from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_global_task_listener_request import (
    CreateGlobalTaskListenerRequest,
)
from ...models.global_task_listener_result import GlobalTaskListenerResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: CreateGlobalTaskListenerRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/global-listeners/user-task"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GlobalTaskListenerResult | ProblemDetail | None:
    if response.status_code == 201:
        response_201 = GlobalTaskListenerResult.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 409:
        response_409 = ProblemDetail.from_dict(response.json())
        return response_409
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
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: CreateGlobalTaskListenerRequest
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    """Create global user task listener

     Create a new global user task listener.

    Args:
        body (CreateGlobalTaskListenerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalTaskListenerResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateGlobalTaskListenerRequest,
    **kwargs: Any,
) -> GlobalTaskListenerResult:
    """Create global user task listener

     Create a new global user task listener.

    Args:
        body (CreateGlobalTaskListenerRequest):

    Raises:
        errors.CreateGlobalTaskListenerBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateGlobalTaskListenerUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateGlobalTaskListenerForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateGlobalTaskListenerConflict: If the response status code is 409. A global listener with this id already exists.
        errors.CreateGlobalTaskListenerInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateGlobalTaskListenerServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalTaskListenerResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateGlobalTaskListenerBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateGlobalTaskListenerUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateGlobalTaskListenerForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateGlobalTaskListenerConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateGlobalTaskListenerInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateGlobalTaskListenerServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalTaskListenerResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: CreateGlobalTaskListenerRequest
) -> Response[GlobalTaskListenerResult | ProblemDetail]:
    """Create global user task listener

     Create a new global user task listener.

    Args:
        body (CreateGlobalTaskListenerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalTaskListenerResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateGlobalTaskListenerRequest,
    **kwargs: Any,
) -> GlobalTaskListenerResult:
    """Create global user task listener

     Create a new global user task listener.

    Args:
        body (CreateGlobalTaskListenerRequest):

    Raises:
        errors.CreateGlobalTaskListenerBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateGlobalTaskListenerUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.CreateGlobalTaskListenerForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateGlobalTaskListenerConflict: If the response status code is 409. A global listener with this id already exists.
        errors.CreateGlobalTaskListenerInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateGlobalTaskListenerServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalTaskListenerResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateGlobalTaskListenerBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.CreateGlobalTaskListenerUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateGlobalTaskListenerForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateGlobalTaskListenerConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateGlobalTaskListenerInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateGlobalTaskListenerServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalTaskListenerResult, response.parsed)
