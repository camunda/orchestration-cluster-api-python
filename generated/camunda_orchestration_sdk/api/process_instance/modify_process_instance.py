from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.modify_process_instance_data import ModifyProcessInstanceData
from ...models.modify_process_instance_response_400 import (
    ModifyProcessInstanceResponse400,
)
from ...models.modify_process_instance_response_404 import (
    ModifyProcessInstanceResponse404,
)
from ...models.modify_process_instance_response_500 import (
    ModifyProcessInstanceResponse500,
)
from ...models.modify_process_instance_response_503 import (
    ModifyProcessInstanceResponse503,
)
from ...types import Response


def _get_kwargs(
    process_instance_key: str, *, body: ModifyProcessInstanceData
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-instances/{process_instance_key}/modification".format(
            process_instance_key=quote(str(process_instance_key), safe="")
        ),
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | ModifyProcessInstanceResponse400
    | ModifyProcessInstanceResponse404
    | ModifyProcessInstanceResponse500
    | ModifyProcessInstanceResponse503
    | None
):
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ModifyProcessInstanceResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = ModifyProcessInstanceResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ModifyProcessInstanceResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ModifyProcessInstanceResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any
    | ModifyProcessInstanceResponse400
    | ModifyProcessInstanceResponse404
    | ModifyProcessInstanceResponse500
    | ModifyProcessInstanceResponse503
]:
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
    body: ModifyProcessInstanceData,
) -> Response[
    Any
    | ModifyProcessInstanceResponse400
    | ModifyProcessInstanceResponse404
    | ModifyProcessInstanceResponse500
    | ModifyProcessInstanceResponse503
]:
    """Modify process instance

     Modifies a running process instance.
    This request can contain multiple instructions to activate an element of the process or
    to terminate an active instance of an element.

    Use this to repair a process instance that is stuck on an element or took an unintended path.
    For example, because an external system is not available or doesn't respond as expected.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (ModifyProcessInstanceData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ModifyProcessInstanceResponse400 | ModifyProcessInstanceResponse404 | ModifyProcessInstanceResponse500 | ModifyProcessInstanceResponse503]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ModifyProcessInstanceData,
    **kwargs: Any,
) -> None:
    """Modify process instance

     Modifies a running process instance.
    This request can contain multiple instructions to activate an element of the process or
    to terminate an active instance of an element.

    Use this to repair a process instance that is stuck on an element or took an unintended path.
    For example, because an external system is not available or doesn't respond as expected.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (ModifyProcessInstanceData):

    Raises:
        errors.ModifyProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.ModifyProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
        errors.ModifyProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ModifyProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        process_instance_key=process_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ModifyProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse400, response.parsed),
            )
        if response.status_code == 404:
            raise errors.ModifyProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.ModifyProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.ModifyProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ModifyProcessInstanceData,
) -> Response[
    Any
    | ModifyProcessInstanceResponse400
    | ModifyProcessInstanceResponse404
    | ModifyProcessInstanceResponse500
    | ModifyProcessInstanceResponse503
]:
    """Modify process instance

     Modifies a running process instance.
    This request can contain multiple instructions to activate an element of the process or
    to terminate an active instance of an element.

    Use this to repair a process instance that is stuck on an element or took an unintended path.
    For example, because an external system is not available or doesn't respond as expected.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (ModifyProcessInstanceData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ModifyProcessInstanceResponse400 | ModifyProcessInstanceResponse404 | ModifyProcessInstanceResponse500 | ModifyProcessInstanceResponse503]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ModifyProcessInstanceData,
    **kwargs: Any,
) -> None:
    """Modify process instance

     Modifies a running process instance.
    This request can contain multiple instructions to activate an element of the process or
    to terminate an active instance of an element.

    Use this to repair a process instance that is stuck on an element or took an unintended path.
    For example, because an external system is not available or doesn't respond as expected.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.
        body (ModifyProcessInstanceData):

    Raises:
        errors.ModifyProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.ModifyProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
        errors.ModifyProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ModifyProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        process_instance_key=process_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ModifyProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse400, response.parsed),
            )
        if response.status_code == 404:
            raise errors.ModifyProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.ModifyProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse500, response.parsed),
            )
        if response.status_code == 503:
            raise errors.ModifyProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ModifyProcessInstanceResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
