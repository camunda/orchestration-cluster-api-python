from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_process_instance_data_type_0 import DeleteProcessInstanceDataType0
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    process_instance_key: str,
    *,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-instances/{process_instance_key}/deletion".format(
            process_instance_key=quote(str(process_instance_key), safe="")
        ),
    }
    if isinstance(body, DeleteProcessInstanceDataType0):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Delete process instance

     Deletes a process instance. Only instances that are completed or terminated can be deleted.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (DeleteProcessInstanceDataType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Delete process instance

     Deletes a process instance. Only instances that are completed or terminated can be deleted.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (DeleteProcessInstanceDataType0 | None | Unset):

    Raises:
        errors.DeleteProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
        errors.DeleteProcessInstanceConflict: If the response status code is 409. The process instance is not in a completed or terminated state and cannot be deleted.
        errors.DeleteProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        process_instance_key=process_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteProcessInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteProcessInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.DeleteProcessInstanceConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Delete process instance

     Deletes a process instance. Only instances that are completed or terminated can be deleted.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (DeleteProcessInstanceDataType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Delete process instance

     Deletes a process instance. Only instances that are completed or terminated can be deleted.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (DeleteProcessInstanceDataType0 | None | Unset):

    Raises:
        errors.DeleteProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
        errors.DeleteProcessInstanceConflict: If the response status code is 409. The process instance is not in a completed or terminated state and cannot be deleted.
        errors.DeleteProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        process_instance_key=process_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteProcessInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteProcessInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.DeleteProcessInstanceConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
