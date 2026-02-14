from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_instance_response_200 import GetProcessInstanceResponse200
from ...models.get_process_instance_response_400 import GetProcessInstanceResponse400
from ...models.get_process_instance_response_401 import GetProcessInstanceResponse401
from ...models.get_process_instance_response_403 import GetProcessInstanceResponse403
from ...models.get_process_instance_response_404 import GetProcessInstanceResponse404
from ...models.get_process_instance_response_500 import GetProcessInstanceResponse500
from ...types import Response


def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/process-instances/{process_instance_key}".format(
            process_instance_key=quote(str(process_instance_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetProcessInstanceResponse200
    | GetProcessInstanceResponse400
    | GetProcessInstanceResponse401
    | GetProcessInstanceResponse403
    | GetProcessInstanceResponse404
    | GetProcessInstanceResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetProcessInstanceResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessInstanceResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessInstanceResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessInstanceResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetProcessInstanceResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetProcessInstanceResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetProcessInstanceResponse200
    | GetProcessInstanceResponse400
    | GetProcessInstanceResponse401
    | GetProcessInstanceResponse403
    | GetProcessInstanceResponse404
    | GetProcessInstanceResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetProcessInstanceResponse200
    | GetProcessInstanceResponse400
    | GetProcessInstanceResponse401
    | GetProcessInstanceResponse403
    | GetProcessInstanceResponse404
    | GetProcessInstanceResponse500
]:
    """Get process instance

     Get the process instance by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceResponse200 | GetProcessInstanceResponse400 | GetProcessInstanceResponse401 | GetProcessInstanceResponse403 | GetProcessInstanceResponse404 | GetProcessInstanceResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetProcessInstanceResponse200:
    """Get process instance

     Get the process instance by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceNotFound: If the response status code is 404. The process instance with the given key was not found.
        errors.GetProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetProcessInstanceResponse200"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceResponse200, response.parsed)


async def asyncio_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetProcessInstanceResponse200
    | GetProcessInstanceResponse400
    | GetProcessInstanceResponse401
    | GetProcessInstanceResponse403
    | GetProcessInstanceResponse404
    | GetProcessInstanceResponse500
]:
    """Get process instance

     Get the process instance by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessInstanceResponse200 | GetProcessInstanceResponse400 | GetProcessInstanceResponse401 | GetProcessInstanceResponse403 | GetProcessInstanceResponse404 | GetProcessInstanceResponse500]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetProcessInstanceResponse200:
    """Get process instance

     Get the process instance by the process instance key.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceNotFound: If the response status code is 404. The process instance with the given key was not found.
        errors.GetProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetProcessInstanceResponse200"""
    response = await asyncio_detailed(
        process_instance_key=process_instance_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessInstanceResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessInstanceResponse200, response.parsed)
