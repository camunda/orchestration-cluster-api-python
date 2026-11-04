from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.user_task_lookup_request import UserTaskLookupRequest
from ...models.user_task_lookup_result import UserTaskLookupResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_task_key: str, *, body: UserTaskLookupRequest | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user-tasks/{user_task_key}/lookup".format(
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
) -> ProblemDetail | UserTaskLookupResult | None:
    if response.status_code == 200:
        response_200 = UserTaskLookupResult.from_dict(response.json())
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
) -> Response[ProblemDetail | UserTaskLookupResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
) -> Response[ProblemDetail | UserTaskLookupResult]:
    """Look up an active user task (alpha)

     Returns an active user task together with the variables visible to it, read from the
    engine's state instead of secondary storage. The task and its variables are read at the
    same point in processing, so they are consistent with each other and with any command the
    engine has already processed, for example the completion of a previous task.

    The response includes the task's lifecycle `state`. Use it to interpret the returned
    values: while a change to the task is in progress, the task fields and variables are the
    ones from before the change, and `state` names the pending change. For example, with
    `ASSIGNING` the returned `assignee` is still the previous one, because task listeners can
    deny the new assignment; with `COMPLETING` the variables don't include the ones sent with
    the completion yet.

    Only active tasks can be looked up. The lookup returns 404 when the task doesn't exist,
    when it was already completed or canceled (use the user task search for those), or when it
    belongs to a tenant the caller isn't assigned to. It returns 409 when the task's process
    instance is banned: an instance that hit an unrecoverable error and can only be canceled.

    Each lookup is processed by the engine. Use it when a task is opened, not for polling.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskLookupRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserTaskLookupResult]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserTaskLookupResult:
    """Look up an active user task (alpha)

     Returns an active user task together with the variables visible to it, read from the
    engine's state instead of secondary storage. The task and its variables are read at the
    same point in processing, so they are consistent with each other and with any command the
    engine has already processed, for example the completion of a previous task.

    The response includes the task's lifecycle `state`. Use it to interpret the returned
    values: while a change to the task is in progress, the task fields and variables are the
    ones from before the change, and `state` names the pending change. For example, with
    `ASSIGNING` the returned `assignee` is still the previous one, because task listeners can
    deny the new assignment; with `COMPLETING` the variables don't include the ones sent with
    the completion yet.

    Only active tasks can be looked up. The lookup returns 404 when the task doesn't exist,
    when it was already completed or canceled (use the user task search for those), or when it
    belongs to a tenant the caller isn't assigned to. It returns 409 when the task's process
    instance is banned: an instance that hit an unrecoverable error and can only be canceled.

    Each lookup is processed by the engine. Use it when a task is opened, not for polling.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskLookupRequest | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. No active user task with the given key is visible to the caller: the task doesn't exist, was already completed or canceled, or belongs to a tenant the caller isn't assigned to.
        errors.ConflictError: If the response status code is 409. The user task can't be looked up because its process instance is banned: it hit an unrecoverable error and can only be canceled. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserTaskLookupResult"""
    response = sync_detailed(user_task_key=user_task_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="lookup_user_task"
        )
    assert response.parsed is not None
    return cast(UserTaskLookupResult, response.parsed)


async def asyncio_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
) -> Response[ProblemDetail | UserTaskLookupResult]:
    """Look up an active user task (alpha)

     Returns an active user task together with the variables visible to it, read from the
    engine's state instead of secondary storage. The task and its variables are read at the
    same point in processing, so they are consistent with each other and with any command the
    engine has already processed, for example the completion of a previous task.

    The response includes the task's lifecycle `state`. Use it to interpret the returned
    values: while a change to the task is in progress, the task fields and variables are the
    ones from before the change, and `state` names the pending change. For example, with
    `ASSIGNING` the returned `assignee` is still the previous one, because task listeners can
    deny the new assignment; with `COMPLETING` the variables don't include the ones sent with
    the completion yet.

    Only active tasks can be looked up. The lookup returns 404 when the task doesn't exist,
    when it was already completed or canceled (use the user task search for those), or when it
    belongs to a tenant the caller isn't assigned to. It returns 409 when the task's process
    instance is banned: an instance that hit an unrecoverable error and can only be canceled.

    Each lookup is processed by the engine. Use it when a task is opened, not for polling.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskLookupRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UserTaskLookupResult]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str,
    *,
    client: AuthenticatedClient,
    body: UserTaskLookupRequest | Unset = UNSET,
    **kwargs: Any,
) -> UserTaskLookupResult:
    """Look up an active user task (alpha)

     Returns an active user task together with the variables visible to it, read from the
    engine's state instead of secondary storage. The task and its variables are read at the
    same point in processing, so they are consistent with each other and with any command the
    engine has already processed, for example the completion of a previous task.

    The response includes the task's lifecycle `state`. Use it to interpret the returned
    values: while a change to the task is in progress, the task fields and variables are the
    ones from before the change, and `state` names the pending change. For example, with
    `ASSIGNING` the returned `assignee` is still the previous one, because task listeners can
    deny the new assignment; with `COMPLETING` the variables don't include the ones sent with
    the completion yet.

    Only active tasks can be looked up. The lookup returns 404 when the task doesn't exist,
    when it was already completed or canceled (use the user task search for those), or when it
    belongs to a tenant the caller isn't assigned to. It returns 409 when the task's process
    instance is banned: an instance that hit an unrecoverable error and can only be canceled.

    Each lookup is processed by the engine. Use it when a task is opened, not for polling.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskLookupRequest | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. No active user task with the given key is visible to the caller: the task doesn't exist, was already completed or canceled, or belongs to a tenant the caller isn't assigned to.
        errors.ConflictError: If the response status code is 409. The user task can't be looked up because its process instance is banned: it hit an unrecoverable error and can only be canceled. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UserTaskLookupResult"""
    response = await asyncio_detailed(
        user_task_key=user_task_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="lookup_user_task",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="lookup_user_task"
        )
    assert response.parsed is not None
    return cast(UserTaskLookupResult, response.parsed)
