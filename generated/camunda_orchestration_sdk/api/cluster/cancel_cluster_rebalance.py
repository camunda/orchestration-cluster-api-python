from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.rebalance_cancellation_response import RebalanceCancellationResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "delete", "url": "/cluster/v2/rebalance"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | RebalanceCancellationResponse | None:
    if response.status_code == 200:
        response_200 = RebalanceCancellationResponse.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 502:
        response_502 = ProblemDetail.from_dict(response.json())
        return response_502
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if response.status_code == 504:
        response_504 = ProblemDetail.from_dict(response.json())
        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | RebalanceCancellationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RebalanceCancellationResponse]:
    """Stop the running rebalance

     Asks the running rebalance to stop once the transfer in flight has finished. Partitions already
    transferred keep their new leaders, and those the rebalance had not yet reached keep their current
    ones.

    Cancellation requests are idempotent and always accepted. The `wasRunning` response field can be
    used to distinguish a cancellation that found a running rebalance from one that did not.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | RebalanceCancellationResponse]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RebalanceCancellationResponse:
    """Stop the running rebalance

     Asks the running rebalance to stop once the transfer in flight has finished. Partitions already
    transferred keep their new leaders, and those the rebalance had not yet reached keep their current
    ones.

    Cancellation requests are idempotent and always accepted. The `wasRunning` response field can be
    used to distinguish a cancellation that found a running rebalance from one that did not.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.BadGatewayError: If the response status code is 502. The coordinator was reached, but its response was absent or unusable.
        errors.ServiceUnavailableError: If the response status code is 503. No coordinator is currently available or reachable.
        errors.GatewayTimeoutError: If the response status code is 504. The coordinator did not answer before the request timeout.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        RebalanceCancellationResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="cancel_cluster_rebalance",
        )
    assert response.parsed is not None
    return cast(RebalanceCancellationResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[ProblemDetail | RebalanceCancellationResponse]:
    """Stop the running rebalance

     Asks the running rebalance to stop once the transfer in flight has finished. Partitions already
    transferred keep their new leaders, and those the rebalance had not yet reached keep their current
    ones.

    Cancellation requests are idempotent and always accepted. The `wasRunning` response field can be
    used to distinguish a cancellation that found a running rebalance from one that did not.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | RebalanceCancellationResponse]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, **kwargs: Any
) -> RebalanceCancellationResponse:
    """Stop the running rebalance

     Asks the running rebalance to stop once the transfer in flight has finished. Partitions already
    transferred keep their new leaders, and those the rebalance had not yet reached keep their current
    ones.

    Cancellation requests are idempotent and always accepted. The `wasRunning` response field can be
    used to distinguish a cancellation that found a running rebalance from one that did not.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.BadGatewayError: If the response status code is 502. The coordinator was reached, but its response was absent or unusable.
        errors.ServiceUnavailableError: If the response status code is 503. No coordinator is currently available or reachable.
        errors.GatewayTimeoutError: If the response status code is 504. The coordinator did not answer before the request timeout.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        RebalanceCancellationResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="cancel_cluster_rebalance",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="cancel_cluster_rebalance",
        )
    assert response.parsed is not None
    return cast(RebalanceCancellationResponse, response.parsed)
