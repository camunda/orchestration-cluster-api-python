import datetime
from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_job_statistics_query_result import GlobalJobStatisticsQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, from_: datetime.datetime, to: datetime.datetime, job_type: str | Unset = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    json_from_ = from_.isoformat()
    params["from"] = json_from_
    json_to = to.isoformat()
    params["to"] = json_to
    params["jobType"] = job_type
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/statistics/global",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GlobalJobStatisticsQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = GlobalJobStatisticsQueryResult.from_dict(response.json())
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
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]:
    """Global job statistics

     Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
    jobType.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        job_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalJobStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(from_=from_, to=to, job_type=job_type)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
    **kwargs: Any,
) -> GlobalJobStatisticsQueryResult:
    """Global job statistics

     Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
    jobType.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        job_type (str | Unset):

    Raises:
        errors.GetGlobalJobStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetGlobalJobStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalJobStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalJobStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalJobStatisticsQueryResult"""
    response = sync_detailed(client=client, from_=from_, to=to, job_type=job_type)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalJobStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetGlobalJobStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalJobStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalJobStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalJobStatisticsQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
) -> Response[GlobalJobStatisticsQueryResult | ProblemDetail]:
    """Global job statistics

     Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
    jobType.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        job_type (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GlobalJobStatisticsQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(from_=from_, to=to, job_type=job_type)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime,
    to: datetime.datetime,
    job_type: str | Unset = UNSET,
    **kwargs: Any,
) -> GlobalJobStatisticsQueryResult:
    """Global job statistics

     Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
    jobType.

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        job_type (str | Unset):

    Raises:
        errors.GetGlobalJobStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetGlobalJobStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalJobStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalJobStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GlobalJobStatisticsQueryResult"""
    response = await asyncio_detailed(
        client=client, from_=from_, to=to, job_type=job_type
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalJobStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetGlobalJobStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalJobStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalJobStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GlobalJobStatisticsQueryResult, response.parsed)
