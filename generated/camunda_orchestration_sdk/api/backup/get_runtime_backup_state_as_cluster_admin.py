from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_runtime_backup_state import ClusterRuntimeBackupState
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(*, physical_tenant_id: str | Unset = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cluster/v2/backups/runtime/state",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterRuntimeBackupState | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClusterRuntimeBackupState.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
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
) -> Response[ClusterRuntimeBackupState | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, physical_tenant_id: str | Unset = UNSET
) -> Response[ClusterRuntimeBackupState | ProblemDetail]:
    """Get runtime backup state across physical tenants

     Reports the checkpoint and backup state of every partition of every physical tenant of the cluster,
    or of the one named by `physicalTenantId`, grouped by physical tenant. Checkpoint ids and log
    positions only mean anything within one physical tenant's partitions, so nothing is aggregated
    across tenants.

    The request is all-or-nothing: a physical tenant whose state cannot be read fails the whole request
    rather than contributing an empty section, which an operator making a delete or restore decision
    could not tell apart from \\"nothing to report yet\\". Narrow the request with `physicalTenantId` to
    read the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime/state` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterRuntimeBackupState | ProblemDetail]
    """
    kwargs = _get_kwargs(physical_tenant_id=physical_tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRuntimeBackupState:
    """Get runtime backup state across physical tenants

     Reports the checkpoint and backup state of every partition of every physical tenant of the cluster,
    or of the one named by `physicalTenantId`, grouped by physical tenant. Checkpoint ids and log
    positions only mean anything within one physical tenant's partitions, so nothing is aggregated
    across tenants.

    The request is all-or-nothing: a physical tenant whose state cannot be read fails the whole request
    rather than contributing an empty section, which an operator making a delete or restore decision
    could not tell apart from \\"nothing to report yet\\". Narrow the request with `physicalTenantId` to
    read the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime/state` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRuntimeBackupState"""
    response = sync_detailed(client=client, physical_tenant_id=physical_tenant_id)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_runtime_backup_state_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterRuntimeBackupState, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, physical_tenant_id: str | Unset = UNSET
) -> Response[ClusterRuntimeBackupState | ProblemDetail]:
    """Get runtime backup state across physical tenants

     Reports the checkpoint and backup state of every partition of every physical tenant of the cluster,
    or of the one named by `physicalTenantId`, grouped by physical tenant. Checkpoint ids and log
    positions only mean anything within one physical tenant's partitions, so nothing is aggregated
    across tenants.

    The request is all-or-nothing: a physical tenant whose state cannot be read fails the whole request
    rather than contributing an empty section, which an operator making a delete or restore decision
    could not tell apart from \\"nothing to report yet\\". Narrow the request with `physicalTenantId` to
    read the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime/state` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterRuntimeBackupState | ProblemDetail]
    """
    kwargs = _get_kwargs(physical_tenant_id=physical_tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRuntimeBackupState:
    """Get runtime backup state across physical tenants

     Reports the checkpoint and backup state of every partition of every physical tenant of the cluster,
    or of the one named by `physicalTenantId`, grouped by physical tenant. Checkpoint ids and log
    positions only mean anything within one physical tenant's partitions, so nothing is aggregated
    across tenants.

    The request is all-or-nothing: a physical tenant whose state cannot be read fails the whole request
    rather than contributing an empty section, which an operator making a delete or restore decision
    could not tell apart from \\"nothing to report yet\\". Narrow the request with `physicalTenantId` to
    read the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime/state` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRuntimeBackupState"""
    response = await asyncio_detailed(
        client=client, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_runtime_backup_state_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_runtime_backup_state_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterRuntimeBackupState, response.parsed)
