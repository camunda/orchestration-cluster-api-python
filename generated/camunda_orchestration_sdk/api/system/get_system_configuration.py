from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.system_configuration_response import SystemConfigurationResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/system/configuration"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SystemConfigurationResponse | None:
    if response.status_code == 200:
        response_200 = SystemConfigurationResponse.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SystemConfigurationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | SystemConfigurationResponse]:
    """System configuration (alpha)

     Returns the current system configuration. The response is an envelope
    that groups settings by feature area.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | SystemConfigurationResponse]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> SystemConfigurationResponse:
    """System configuration (alpha)

     Returns the current system configuration. The response is an envelope
    that groups settings by feature area.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SystemConfigurationResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_system_configuration",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_system_configuration",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_system_configuration",
        )
    assert response.parsed is not None
    return cast(SystemConfigurationResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | SystemConfigurationResponse]:
    """System configuration (alpha)

     Returns the current system configuration. The response is an envelope
    that groups settings by feature area.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | SystemConfigurationResponse]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> SystemConfigurationResponse:
    """System configuration (alpha)

     Returns the current system configuration. The response is an envelope
    that groups settings by feature area.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SystemConfigurationResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_system_configuration",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_system_configuration",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_system_configuration",
        )
    assert response.parsed is not None
    return cast(SystemConfigurationResponse, response.parsed)
