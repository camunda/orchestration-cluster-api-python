from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clock_add_request import ClockAddRequest
from ...models.clock_result import ClockResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: ClockAddRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/clock/add"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClockResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClockResult.from_dict(response.json())
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
) -> Response[ClockResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: ClockAddRequest
) -> Response[ClockResult | ProblemDetail]:
    """Add time to internal clock

     Moves the Zeebe engine's internal clock forward or backward by the given offset.
    Unlike pinning, the clock keeps ticking in real time after the offset is added. If the
    clock is pinned, it stays pinned and moves to the pinned time plus the offset.

    Each request adds to the time of the clock, so adding `PT1H` twice moves the clock two
    hours ahead. Use `POST /v2/clock/reset` to remove all added time and return the clock to
    the system time.

    The response contains the new time of the clock. The change reaches all partitions
    shortly after it is accepted, so a request sent right after it may still use the previous
    time.

    Args:
        body (ClockAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClockResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: ClockAddRequest, **kwargs: Any
) -> ClockResult:
    """Add time to internal clock

     Moves the Zeebe engine's internal clock forward or backward by the given offset.
    Unlike pinning, the clock keeps ticking in real time after the offset is added. If the
    clock is pinned, it stays pinned and moves to the pinned time plus the offset.

    Each request adds to the time of the clock, so adding `PT1H` twice moves the clock two
    hours ahead. Use `POST /v2/clock/reset` to remove all added time and return the clock to
    the system time.

    The response contains the new time of the clock. The change reaches all partitions
    shortly after it is accepted, so a request sent right after it may still use the previous
    time.

    Args:
        body (ClockAddRequest):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClockResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="add_clock"
        )
    assert response.parsed is not None
    return cast(ClockResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ClockAddRequest
) -> Response[ClockResult | ProblemDetail]:
    """Add time to internal clock

     Moves the Zeebe engine's internal clock forward or backward by the given offset.
    Unlike pinning, the clock keeps ticking in real time after the offset is added. If the
    clock is pinned, it stays pinned and moves to the pinned time plus the offset.

    Each request adds to the time of the clock, so adding `PT1H` twice moves the clock two
    hours ahead. Use `POST /v2/clock/reset` to remove all added time and return the clock to
    the system time.

    The response contains the new time of the clock. The change reaches all partitions
    shortly after it is accepted, so a request sent right after it may still use the previous
    time.

    Args:
        body (ClockAddRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClockResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: ClockAddRequest, **kwargs: Any
) -> ClockResult:
    """Add time to internal clock

     Moves the Zeebe engine's internal clock forward or backward by the given offset.
    Unlike pinning, the clock keeps ticking in real time after the offset is added. If the
    clock is pinned, it stays pinned and moves to the pinned time plus the offset.

    Each request adds to the time of the clock, so adding `PT1H` twice moves the clock two
    hours ahead. Use `POST /v2/clock/reset` to remove all added time and return the clock to
    the system time.

    The response contains the new time of the clock. The change reaches all partitions
    shortly after it is accepted, so a request sent right after it may still use the previous
    time.

    Args:
        body (ClockAddRequest):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClockResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="add_clock",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="add_clock"
        )
    assert response.parsed is not None
    return cast(ClockResult, response.parsed)
