from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.license_response import LicenseResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/license"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> LicenseResponse | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = LicenseResponse.from_dict(response.json())
        return response_200
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[LicenseResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[LicenseResponse | ProblemDetail]:
    """Get license status

     Obtains the status of the current Camunda license.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LicenseResponse | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient | Client, **kwargs: Any) -> LicenseResponse:
    """Get license status

     Obtains the status of the current Camunda license.

    Raises:
        errors.GetLicenseInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        LicenseResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 500:
            raise errors.GetLicenseInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(LicenseResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[LicenseResponse | ProblemDetail]:
    """Get license status

     Obtains the status of the current Camunda license.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LicenseResponse | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> LicenseResponse:
    """Get license status

     Obtains the status of the current Camunda license.

    Raises:
        errors.GetLicenseInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        LicenseResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 500:
            raise errors.GetLicenseInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(LicenseResponse, response.parsed)
