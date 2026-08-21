from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_take_runtime_backup_response import (
    ClusterTakeRuntimeBackupResponse,
)
from ...models.problem_detail import ProblemDetail
from ...models.take_runtime_backup_request import TakeRuntimeBackupRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cluster/v2/backups/runtime",
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterTakeRuntimeBackupResponse | ProblemDetail | None:
    if response.status_code == 202:
        response_202 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_202
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_500
    if response.status_code == 502:
        response_502 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_502
    if response.status_code == 503:
        response_503 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_503
    if response.status_code == 504:
        response_504 = ClusterTakeRuntimeBackupResponse.from_dict(response.json())
        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]:
    """Take a runtime backup on one or every physical tenant

     Triggers a runtime backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. A cluster-wide backup is a set of independent per-tenant backups, not an atomic
    snapshot of the cluster: they are neither coordinated nor rolled back together, and each tenant
    stores its own, so the same `backupId` can be used for all of them.

    Every targeted physical tenant must be in the same backup-id mode. `backupId` must be omitted when
    every targeted tenant generates its own ids (because continuous backups and/or a backup or
    checkpoint schedule is enabled for it), and is required when none of them does. A cluster whose
    targeted tenants mix the two modes is rejected with 400 and has to be driven one tenant at a time
    through `POST /v2/backups/runtime`. In generated-id mode each tenant generates its own id, so the
    response reports an id per physical tenant rather than one for the cluster.

    The trigger is all-or-error, and never silent about a partial trigger: if any targeted tenant cannot
    be triggered the response carries an error status, but its body still lists every targeted tenant —
    which ones were triggered, under which `backupId` to monitor or delete them, and why the others
    failed. Nothing is rolled back, so the backups that were triggered keep running and have to be
    deleted explicitly. A request rejected before any tenant was triggered answers with a problem detail
    instead, and nothing is running.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `POST
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeRuntimeBackupRequest | Unset): Request body for taking a runtime backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, physical_tenant_id=physical_tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeRuntimeBackupResponse:
    """Take a runtime backup on one or every physical tenant

     Triggers a runtime backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. A cluster-wide backup is a set of independent per-tenant backups, not an atomic
    snapshot of the cluster: they are neither coordinated nor rolled back together, and each tenant
    stores its own, so the same `backupId` can be used for all of them.

    Every targeted physical tenant must be in the same backup-id mode. `backupId` must be omitted when
    every targeted tenant generates its own ids (because continuous backups and/or a backup or
    checkpoint schedule is enabled for it), and is required when none of them does. A cluster whose
    targeted tenants mix the two modes is rejected with 400 and has to be driven one tenant at a time
    through `POST /v2/backups/runtime`. In generated-id mode each tenant generates its own id, so the
    response reports an id per physical tenant rather than one for the cluster.

    The trigger is all-or-error, and never silent about a partial trigger: if any targeted tenant cannot
    be triggered the response carries an error status, but its body still lists every targeted tenant —
    which ones were triggered, under which `backupId` to monitor or delete them, and why the others
    failed. Nothing is rolled back, so the backups that were triggered keep running and have to be
    deleted explicitly. A request rejected before any tenant was triggered answers with a problem detail
    instead, and nothing is running.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `POST
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeRuntimeBackupRequest | Unset): Request body for taking a runtime backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The request names a `backupId` while at least one targeted physical tenant generates its own ids, or omits it while at least one does not, or the id is not a positive number. No tenant was triggered. A targeted tenant that rejects the request as invalid during the fan-out answers with the same status but the cluster body, listing the tenants that were triggered.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster, so no tenant was triggered.
        errors.ConflictError: If the response status code is 409. At least one targeted physical tenant already holds a backup with this id or a higher one. Backups are triggered without a preceding check, so the tenants that accepted the id are listed in the body and keep running; delete them before retrying.
        errors.InternalServerErrorError: If the response status code is 500. At least one targeted physical tenant could not be triggered, and the failures do not agree on a single status. The body lists the tenants that were triggered and keep running.
        errors.BadGatewayError: If the response status code is 502. The connection to the broker was cut mid-flight on at least one targeted physical tenant, which may or may not have accepted the request. Those tenants are reported as `UNKNOWN` with the id to check them under, and the tenants that were triggered keep running.
        errors.ServiceUnavailableError: If the response status code is 503. At least one targeted physical tenant could not be reached. The body lists the tenants that were triggered and keep running.
        errors.GatewayTimeoutError: If the response status code is 504. The request from gateway to broker timed out on at least one targeted physical tenant, which may or may not have accepted it. Those tenants are reported as `UNKNOWN` with the id to check them under, and the tenants that were triggered keep running.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterTakeRuntimeBackupResponse"""
    response = sync_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="take_runtime_backup_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterTakeRuntimeBackupResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]:
    """Take a runtime backup on one or every physical tenant

     Triggers a runtime backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. A cluster-wide backup is a set of independent per-tenant backups, not an atomic
    snapshot of the cluster: they are neither coordinated nor rolled back together, and each tenant
    stores its own, so the same `backupId` can be used for all of them.

    Every targeted physical tenant must be in the same backup-id mode. `backupId` must be omitted when
    every targeted tenant generates its own ids (because continuous backups and/or a backup or
    checkpoint schedule is enabled for it), and is required when none of them does. A cluster whose
    targeted tenants mix the two modes is rejected with 400 and has to be driven one tenant at a time
    through `POST /v2/backups/runtime`. In generated-id mode each tenant generates its own id, so the
    response reports an id per physical tenant rather than one for the cluster.

    The trigger is all-or-error, and never silent about a partial trigger: if any targeted tenant cannot
    be triggered the response carries an error status, but its body still lists every targeted tenant —
    which ones were triggered, under which `backupId` to monitor or delete them, and why the others
    failed. Nothing is rolled back, so the backups that were triggered keep running and have to be
    deleted explicitly. A request rejected before any tenant was triggered answers with a problem detail
    instead, and nothing is running.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `POST
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeRuntimeBackupRequest | Unset): Request body for taking a runtime backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterTakeRuntimeBackupResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, physical_tenant_id=physical_tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TakeRuntimeBackupRequest | Unset = UNSET,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeRuntimeBackupResponse:
    """Take a runtime backup on one or every physical tenant

     Triggers a runtime backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. A cluster-wide backup is a set of independent per-tenant backups, not an atomic
    snapshot of the cluster: they are neither coordinated nor rolled back together, and each tenant
    stores its own, so the same `backupId` can be used for all of them.

    Every targeted physical tenant must be in the same backup-id mode. `backupId` must be omitted when
    every targeted tenant generates its own ids (because continuous backups and/or a backup or
    checkpoint schedule is enabled for it), and is required when none of them does. A cluster whose
    targeted tenants mix the two modes is rejected with 400 and has to be driven one tenant at a time
    through `POST /v2/backups/runtime`. In generated-id mode each tenant generates its own id, so the
    response reports an id per physical tenant rather than one for the cluster.

    The trigger is all-or-error, and never silent about a partial trigger: if any targeted tenant cannot
    be triggered the response carries an error status, but its body still lists every targeted tenant —
    which ones were triggered, under which `backupId` to monitor or delete them, and why the others
    failed. Nothing is rolled back, so the backups that were triggered keep running and have to be
    deleted explicitly. A request rejected before any tenant was triggered answers with a problem detail
    instead, and nothing is running.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `POST
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeRuntimeBackupRequest | Unset): Request body for taking a runtime backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The request names a `backupId` while at least one targeted physical tenant generates its own ids, or omits it while at least one does not, or the id is not a positive number. No tenant was triggered. A targeted tenant that rejects the request as invalid during the fan-out answers with the same status but the cluster body, listing the tenants that were triggered.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster, so no tenant was triggered.
        errors.ConflictError: If the response status code is 409. At least one targeted physical tenant already holds a backup with this id or a higher one. Backups are triggered without a preceding check, so the tenants that accepted the id are listed in the body and keep running; delete them before retrying.
        errors.InternalServerErrorError: If the response status code is 500. At least one targeted physical tenant could not be triggered, and the failures do not agree on a single status. The body lists the tenants that were triggered and keep running.
        errors.BadGatewayError: If the response status code is 502. The connection to the broker was cut mid-flight on at least one targeted physical tenant, which may or may not have accepted the request. Those tenants are reported as `UNKNOWN` with the id to check them under, and the tenants that were triggered keep running.
        errors.ServiceUnavailableError: If the response status code is 503. At least one targeted physical tenant could not be reached. The body lists the tenants that were triggered and keep running.
        errors.GatewayTimeoutError: If the response status code is 504. The request from gateway to broker timed out on at least one targeted physical tenant, which may or may not have accepted it. Those tenants are reported as `UNKNOWN` with the id to check them under, and the tenants that were triggered keep running.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterTakeRuntimeBackupResponse"""
    response = await asyncio_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 502:
            raise errors.BadGatewayError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterTakeRuntimeBackupResponse, response.parsed),
                operation_id="take_runtime_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="take_runtime_backup_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterTakeRuntimeBackupResponse, response.parsed)
