from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_time_series_statistics_query import JobTimeSeriesStatisticsQuery
from ...models.job_time_series_statistics_query_result import (
    JobTimeSeriesStatisticsQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: JobTimeSeriesStatisticsQuery) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/jobs/statistics/time-series"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> JobTimeSeriesStatisticsQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = JobTimeSeriesStatisticsQueryResult.from_dict(response.json())
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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[JobTimeSeriesStatisticsQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: JobTimeSeriesStatisticsQuery
) -> Response[JobTimeSeriesStatisticsQueryResult | ProblemDetail]:
    """Get time-series metrics for a job type

     Returns a list of time-bucketed metrics ordered ascending by time.
    The `from` and `to` fields select the time window of interest.
    Each item in the response corresponds to one time bucket of the requested resolution.

    Args:
        body (JobTimeSeriesStatisticsQuery): Job time-series statistics query.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobTimeSeriesStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: JobTimeSeriesStatisticsQuery,
    **kwargs: Any,
) -> JobTimeSeriesStatisticsQueryResult:
    """Get time-series metrics for a job type

     Returns a list of time-bucketed metrics ordered ascending by time.
    The `from` and `to` fields select the time window of interest.
    Each item in the response corresponds to one time bucket of the requested resolution.

    Args:
        body (JobTimeSeriesStatisticsQuery): Job time-series statistics query.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        JobTimeSeriesStatisticsQueryResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_job_time_series_statistics",
        )
    assert response.parsed is not None
    return cast(JobTimeSeriesStatisticsQueryResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: JobTimeSeriesStatisticsQuery
) -> Response[JobTimeSeriesStatisticsQueryResult | ProblemDetail]:
    """Get time-series metrics for a job type

     Returns a list of time-bucketed metrics ordered ascending by time.
    The `from` and `to` fields select the time window of interest.
    Each item in the response corresponds to one time bucket of the requested resolution.

    Args:
        body (JobTimeSeriesStatisticsQuery): Job time-series statistics query.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobTimeSeriesStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: JobTimeSeriesStatisticsQuery,
    **kwargs: Any,
) -> JobTimeSeriesStatisticsQueryResult:
    """Get time-series metrics for a job type

     Returns a list of time-bucketed metrics ordered ascending by time.
    The `from` and `to` fields select the time window of interest.
    Each item in the response corresponds to one time bucket of the requested resolution.

    Args:
        body (JobTimeSeriesStatisticsQuery): Job time-series statistics query.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        JobTimeSeriesStatisticsQueryResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_job_time_series_statistics",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_job_time_series_statistics",
        )
    assert response.parsed is not None
    return cast(JobTimeSeriesStatisticsQueryResult, response.parsed)
