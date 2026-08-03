from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.exporting_status_response import ExportingStatusResponse
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/exporting"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ExportingStatusResponse | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ExportingStatusResponse.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
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
) -> Response[ExportingStatusResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ExportingStatusResponse | ProblemDetail]:
    """Get exporting status

     Returns the exporting status of the physical tenant, aggregated over every replica of
    every one of its partitions.

    Because pause and resume are applied to all replicas, the status is only a single phase
    if every replica reports that phase; otherwise it is `MIXED`, which means a pause or
    resume is still in flight or was only partially applied. Backup tooling should treat
    only `PAUSED` and `SOFT_PAUSED` as confirmation that exporting is paused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportingStatusResponse | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient, **kwargs: Any) -> ExportingStatusResponse:
    """Get exporting status

     Returns the exporting status of the physical tenant, aggregated over every replica of
    every one of its partitions.

    Because pause and resume are applied to all replicas, the status is only a single phase
    if every replica reports that phase; otherwise it is `MIXED`, which means a pause or
    resume is still in flight or was only partially applied. Backup tooling should treat
    only `PAUSED` and `SOFT_PAUSED` as confirmation that exporting is paused.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ExportingStatusResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_exporting_status"
        )
    assert response.parsed is not None
    return cast(ExportingStatusResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ExportingStatusResponse | ProblemDetail]:
    """Get exporting status

     Returns the exporting status of the physical tenant, aggregated over every replica of
    every one of its partitions.

    Because pause and resume are applied to all replicas, the status is only a single phase
    if every replica reports that phase; otherwise it is `MIXED`, which means a pause or
    resume is still in flight or was only partially applied. Backup tooling should treat
    only `PAUSED` and `SOFT_PAUSED` as confirmation that exporting is paused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportingStatusResponse | ProblemDetail]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> ExportingStatusResponse:
    """Get exporting status

     Returns the exporting status of the physical tenant, aggregated over every replica of
    every one of its partitions.

    Because pause and resume are applied to all replicas, the status is only a single phase
    if every replica reports that phase; otherwise it is `MIXED`, which means a pause or
    resume is still in flight or was only partially applied. Backup tooling should treat
    only `PAUSED` and `SOFT_PAUSED` as confirmation that exporting is paused.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ExportingStatusResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_exporting_status",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_exporting_status"
        )
    assert response.parsed is not None
    return cast(ExportingStatusResponse, response.parsed)
