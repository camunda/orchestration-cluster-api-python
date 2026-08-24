from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_balance_response import ClusterBalanceResponse
from ...models.cluster_rebalance_request import ClusterRebalanceRequest
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: ClusterRebalanceRequest | Unset = UNSET, dry_run: bool | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["dryRun"] = dry_run
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cluster/v2/rebalance",
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterBalanceResponse | ProblemDetail | None:
    if response.status_code == 202:
        response_202 = ClusterBalanceResponse.from_dict(response.json())
        return response_202
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 409:
        response_409 = ProblemDetail.from_dict(response.json())
        return response_409
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
) -> Response[ClusterBalanceResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterBalanceResponse | ProblemDetail]:
    """Trigger a cluster-wide leadership rebalance

     Transfers leadership of every partition that is not led by its highest-priority replica towards that
    replica, one partition at a time. Returns as soon as the rebalance has been accepted (poll `GET
    /cluster/v2/rebalance` to monitor progress).

    Each rebalance can specify overrides for the configured rebalance settings (e.g. maximum replication
    lag to allow). An absent request body means \\"use the configured settings\\".

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        dry_run (bool | Unset):
        body (ClusterRebalanceRequest | Unset): The settings to run a given rebalance with. Every
            setting is optional; an absent request body is equivalent to a body with every field
            absent, and means "use the configured settings".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterBalanceResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, dry_run=dry_run)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterBalanceResponse:
    """Trigger a cluster-wide leadership rebalance

     Transfers leadership of every partition that is not led by its highest-priority replica towards that
    replica, one partition at a time. Returns as soon as the rebalance has been accepted (poll `GET
    /cluster/v2/rebalance` to monitor progress).

    Each rebalance can specify overrides for the configured rebalance settings (e.g. maximum replication
    lag to allow). An absent request body means \\"use the configured settings\\".

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        dry_run (bool | Unset):
        body (ClusterRebalanceRequest | Unset): The settings to run a given rebalance with. Every
            setting is optional; an absent request body is equivalent to a body with every field
            absent, and means "use the configured settings".

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ConflictError: If the response status code is 409. A rebalance or cluster configuration change is already in progress, so there is no settled configuration to plan a rebalance against.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.BadGatewayError: If the response status code is 502. The coordinator was reached, but its response was absent or unusable.
        errors.ServiceUnavailableError: If the response status code is 503. No coordinator is currently available or reachable.
        errors.GatewayTimeoutError: If the response status code is 504. The coordinator did not answer before the request timeout.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterBalanceResponse"""
    response = sync_detailed(client=client, body=body, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="trigger_cluster_rebalance",
        )
    assert response.parsed is not None
    return cast(ClusterBalanceResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterBalanceResponse | ProblemDetail]:
    """Trigger a cluster-wide leadership rebalance

     Transfers leadership of every partition that is not led by its highest-priority replica towards that
    replica, one partition at a time. Returns as soon as the rebalance has been accepted (poll `GET
    /cluster/v2/rebalance` to monitor progress).

    Each rebalance can specify overrides for the configured rebalance settings (e.g. maximum replication
    lag to allow). An absent request body means \\"use the configured settings\\".

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        dry_run (bool | Unset):
        body (ClusterRebalanceRequest | Unset): The settings to run a given rebalance with. Every
            setting is optional; an absent request body is equivalent to a body with every field
            absent, and means "use the configured settings".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterBalanceResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, dry_run=dry_run)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClusterRebalanceRequest | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterBalanceResponse:
    """Trigger a cluster-wide leadership rebalance

     Transfers leadership of every partition that is not led by its highest-priority replica towards that
    replica, one partition at a time. Returns as soon as the rebalance has been accepted (poll `GET
    /cluster/v2/rebalance` to monitor progress).

    Each rebalance can specify overrides for the configured rebalance settings (e.g. maximum replication
    lag to allow). An absent request body means \\"use the configured settings\\".

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        dry_run (bool | Unset):
        body (ClusterRebalanceRequest | Unset): The settings to run a given rebalance with. Every
            setting is optional; an absent request body is equivalent to a body with every field
            absent, and means "use the configured settings".

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ConflictError: If the response status code is 409. A rebalance or cluster configuration change is already in progress, so there is no settled configuration to plan a rebalance against.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.BadGatewayError: If the response status code is 502. The coordinator was reached, but its response was absent or unusable.
        errors.ServiceUnavailableError: If the response status code is 503. No coordinator is currently available or reachable.
        errors.GatewayTimeoutError: If the response status code is 504. The coordinator did not answer before the request timeout.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterBalanceResponse"""
    response = await asyncio_detailed(client=client, body=body, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="trigger_cluster_rebalance",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="trigger_cluster_rebalance",
        )
    assert response.parsed is not None
    return cast(ClusterBalanceResponse, response.parsed)
