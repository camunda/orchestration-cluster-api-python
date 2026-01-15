from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.complete_user_task_data import CompleteUserTaskData
from ...models.complete_user_task_response_400 import CompleteUserTaskResponse400
from ...models.complete_user_task_response_404 import CompleteUserTaskResponse404
from ...models.complete_user_task_response_409 import CompleteUserTaskResponse409
from ...models.complete_user_task_response_500 import CompleteUserTaskResponse500
from ...models.complete_user_task_response_503 import CompleteUserTaskResponse503
from ...types import UNSET, Response, Unset

def _get_kwargs(user_task_key: str, *, body: CompleteUserTaskData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/user-tasks/{user_task_key}/completion'.format(user_task_key=quote(str(user_task_key), safe=''))}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = CompleteUserTaskResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = CompleteUserTaskResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = CompleteUserTaskResponse409.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = CompleteUserTaskResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CompleteUserTaskResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(user_task_key: str, *, client: AuthenticatedClient | Client, body: CompleteUserTaskData | Unset=UNSET) -> Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]:
    """Complete user task

     Completes a user task with the given key.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (CompleteUserTaskData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(user_task_key: str, *, client: AuthenticatedClient | Client, body: CompleteUserTaskData | Unset=UNSET, **kwargs) -> Any:
    """Complete user task

 Completes a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (CompleteUserTaskData | Unset):

Raises:
    errors.CompleteUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CompleteUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.CompleteUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.CompleteUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CompleteUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(user_task_key=user_task_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CompleteUserTaskBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.CompleteUserTaskNotFound(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.CompleteUserTaskConflict(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.CompleteUserTaskInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CompleteUserTaskServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(user_task_key: str, *, client: AuthenticatedClient | Client, body: CompleteUserTaskData | Unset=UNSET) -> Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]:
    """Complete user task

     Completes a user task with the given key.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (CompleteUserTaskData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(user_task_key: str, *, client: AuthenticatedClient | Client, body: CompleteUserTaskData | Unset=UNSET, **kwargs) -> Any:
    """Complete user task

 Completes a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (CompleteUserTaskData | Unset):

Raises:
    errors.CompleteUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CompleteUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.CompleteUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.CompleteUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CompleteUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(user_task_key=user_task_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CompleteUserTaskBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.CompleteUserTaskNotFound(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.CompleteUserTaskConflict(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.CompleteUserTaskInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CompleteUserTaskServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CompleteUserTaskResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed