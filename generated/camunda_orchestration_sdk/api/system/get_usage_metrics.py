import datetime
from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.usage_metrics_response import UsageMetricsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    tenant_id: str | Unset = UNSET,
    with_tenants: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time
    json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time
    params["tenantId"] = tenant_id
    params["withTenants"] = with_tenants
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/system/usage-metrics",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | UsageMetricsResponse | None:
    if response.status_code == 200:
        response_200 = UsageMetricsResponse.from_dict(response.json())
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
) -> Response[ProblemDetail | UsageMetricsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    tenant_id: str | Unset = UNSET,
    with_tenants: bool | Unset = False,
) -> Response[ProblemDetail | UsageMetricsResponse]:
    """Get usage metrics

     Retrieve the usage metrics based on given criteria.

    Args:
        start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
        with_tenants (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UsageMetricsResponse]
    """
    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        tenant_id=tenant_id,
        with_tenants=with_tenants,
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    tenant_id: str | Unset = UNSET,
    with_tenants: bool | Unset = False,
    **kwargs: Any,
) -> UsageMetricsResponse:
    """Get usage metrics

     Retrieve the usage metrics based on given criteria.

    Args:
        start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
        with_tenants (bool | Unset):  Default: False.

    Raises:
        errors.GetUsageMetricsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUsageMetricsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUsageMetricsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUsageMetricsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UsageMetricsResponse"""
    response = sync_detailed(
        client=client,
        start_time=start_time,
        end_time=end_time,
        tenant_id=tenant_id,
        with_tenants=with_tenants,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUsageMetricsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUsageMetricsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUsageMetricsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUsageMetricsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UsageMetricsResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    tenant_id: str | Unset = UNSET,
    with_tenants: bool | Unset = False,
) -> Response[ProblemDetail | UsageMetricsResponse]:
    """Get usage metrics

     Retrieve the usage metrics based on given criteria.

    Args:
        start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
        with_tenants (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | UsageMetricsResponse]
    """
    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        tenant_id=tenant_id,
        with_tenants=with_tenants,
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    tenant_id: str | Unset = UNSET,
    with_tenants: bool | Unset = False,
    **kwargs: Any,
) -> UsageMetricsResponse:
    """Get usage metrics

     Retrieve the usage metrics based on given criteria.

    Args:
        start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
        tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
        with_tenants (bool | Unset):  Default: False.

    Raises:
        errors.GetUsageMetricsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetUsageMetricsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetUsageMetricsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetUsageMetricsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        UsageMetricsResponse"""
    response = await asyncio_detailed(
        client=client,
        start_time=start_time,
        end_time=end_time,
        tenant_id=tenant_id,
        with_tenants=with_tenants,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetUsageMetricsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetUsageMetricsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetUsageMetricsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetUsageMetricsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(UsageMetricsResponse, response.parsed)
