from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_error_statistics_query import JobErrorStatisticsQuery
from ...models.job_error_statistics_query_result import JobErrorStatisticsQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: JobErrorStatisticsQuery) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/jobs/statistics/errors"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> JobErrorStatisticsQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = JobErrorStatisticsQueryResult.from_dict(response.json())
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
) -> Response[JobErrorStatisticsQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: JobErrorStatisticsQuery
) -> Response[JobErrorStatisticsQueryResult | ProblemDetail]:
    """Get error metrics for a job type

     Returns aggregated metrics per error for the given jobType.

    Args:
        body (JobErrorStatisticsQuery): Job error statistics query.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobErrorStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: JobErrorStatisticsQuery,
    **kwargs: Any,
) -> JobErrorStatisticsQueryResult:
    """Get error metrics for a job type

     Returns aggregated metrics per error for the given jobType.

    Args:
        body (JobErrorStatisticsQuery): Job error statistics query.

    Raises:
        errors.GetJobErrorStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetJobErrorStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetJobErrorStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetJobErrorStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        JobErrorStatisticsQueryResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetJobErrorStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetJobErrorStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetJobErrorStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetJobErrorStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(JobErrorStatisticsQueryResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: JobErrorStatisticsQuery
) -> Response[JobErrorStatisticsQueryResult | ProblemDetail]:
    """Get error metrics for a job type

     Returns aggregated metrics per error for the given jobType.

    Args:
        body (JobErrorStatisticsQuery): Job error statistics query.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobErrorStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: JobErrorStatisticsQuery,
    **kwargs: Any,
) -> JobErrorStatisticsQueryResult:
    """Get error metrics for a job type

     Returns aggregated metrics per error for the given jobType.

    Args:
        body (JobErrorStatisticsQuery): Job error statistics query.

    Raises:
        errors.GetJobErrorStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetJobErrorStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetJobErrorStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetJobErrorStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        JobErrorStatisticsQueryResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetJobErrorStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetJobErrorStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetJobErrorStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetJobErrorStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(JobErrorStatisticsQueryResult, response.parsed)
