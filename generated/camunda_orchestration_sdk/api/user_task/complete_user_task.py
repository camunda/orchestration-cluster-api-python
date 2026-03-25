from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_task_completion_request import UserTaskCompletionRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_task_key: str, *, body: UserTaskCompletionRequest | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user-tasks/{user_task_key}/completion".format(
            user_task_key=quote(str(user_task_key), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = ProblemDetail.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if response.status_code == 504:
        response_504 = ProblemDetail.from_dict(response.json())
        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskCompletionRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Complete user task

     Completes a user task with the given key. Completion waits for blocking task listeners on this
    lifecycle transition. If listener processing is delayed beyond the request timeout, this endpoint
    can return 504. Other gateway timeout causes are also possible. Retry with backoff and inspect
    listener worker availability and logs when this repeats.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskCompletionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskCompletionRequest | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Complete user task

     Completes a user task with the given key. Completion waits for blocking task listeners on this
    lifecycle transition. If listener processing is delayed beyond the request timeout, this endpoint
    can return 504. Other gateway timeout causes are also possible. Retry with backoff and inspect
    listener worker availability and logs when this repeats.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskCompletionRequest | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.NotFoundError: If the response status code is 404. The user task with the given key was not found.
        errors.ConflictError: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.GatewayTimeoutError: If the response status code is 504. The request timed out between the gateway and the broker. For these endpoints, this often happens when user task listeners are configured and the corresponding listener job is not completed within the request timeout. Common causes include no available job workers for the listener type, busy or crashed job workers, or delayed job completion. As with any gateway timeout, general timeout causes (for example transient network issues) can also result in a 504 response. Troubleshooting: - verify that job workers for the listener type are running and healthy - check worker logs for crashes, retries, and completion failures - check network connectivity between workers, gateway, and broker - retry with backoff after transient failures - fail without retries if a problem persists
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(user_task_key=user_task_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="complete_user_task"
        )
    return None


async def asyncio_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskCompletionRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Complete user task

     Completes a user task with the given key. Completion waits for blocking task listeners on this
    lifecycle transition. If listener processing is delayed beyond the request timeout, this endpoint
    can return 504. Other gateway timeout causes are also possible. Retry with backoff and inspect
    listener worker availability and logs when this repeats.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskCompletionRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskCompletionRequest | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Complete user task

     Completes a user task with the given key. Completion waits for blocking task listeners on this
    lifecycle transition. If listener processing is delayed beyond the request timeout, this endpoint
    can return 504. Other gateway timeout causes are also possible. Retry with backoff and inspect
    listener worker availability and logs when this repeats.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskCompletionRequest | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.NotFoundError: If the response status code is 404. The user task with the given key was not found.
        errors.ConflictError: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.GatewayTimeoutError: If the response status code is 504. The request timed out between the gateway and the broker. For these endpoints, this often happens when user task listeners are configured and the corresponding listener job is not completed within the request timeout. Common causes include no available job workers for the listener type, busy or crashed job workers, or delayed job completion. As with any gateway timeout, general timeout causes (for example transient network issues) can also result in a 504 response. Troubleshooting: - verify that job workers for the listener type are running and healthy - check worker logs for crashes, retries, and completion failures - check network connectivity between workers, gateway, and broker - retry with backoff after transient failures - fail without retries if a problem persists
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        user_task_key=user_task_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="complete_user_task",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="complete_user_task"
        )
    return None
