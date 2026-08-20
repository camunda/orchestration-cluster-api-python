from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_take_history_backup_response import (
    ClusterTakeHistoryBackupResponse,
)
from ...models.problem_detail import ProblemDetail
from ...models.take_history_backup_request import TakeHistoryBackupRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: TakeHistoryBackupRequest, physical_tenant_id: str | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cluster/v2/backups/history",
        "params": params,
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterTakeHistoryBackupResponse | ProblemDetail | None:
    if response.status_code == 202:
        response_202 = ClusterTakeHistoryBackupResponse.from_dict(response.json())
        return response_202
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = ProblemDetail.from_dict(response.json())
        return response_409
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
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]:
    """Take a history backup on one or every physical tenant

     Triggers a history backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. Every targeted tenant uses the same caller-supplied `backupId`, but the backups
    are independent: they are neither coordinated nor rolled back together.

    The request is all-or-nothing: the `backupId` is checked on every targeted tenant before any
    snapshot is scheduled, so a tenant that already holds this id, or that cannot be reached, fails the
    whole request and no backup is started anywhere. There is no aggregated cluster-level state in the
    response.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `POST /v2/backups/history` to act as a
    single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterTakeHistoryBackupResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, physical_tenant_id=physical_tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeHistoryBackupResponse:
    """Take a history backup on one or every physical tenant

     Triggers a history backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. Every targeted tenant uses the same caller-supplied `backupId`, but the backups
    are independent: they are neither coordinated nor rolled back together.

    The request is all-or-nothing: the `backupId` is checked on every targeted tenant before any
    snapshot is scheduled, so a tenant that already holds this id, or that cannot be reached, fails the
    whole request and no backup is started anywhere. There is no aggregated cluster-level state in the
    response.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `POST /v2/backups/history` to act as a
    single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups, or a targeted physical tenant's snapshot repository is absent from the store — configured under a name the store does not have, or not configured at all. Both are deployment faults the caller cannot correct by changing its request; narrow the request with `physicalTenantId` to work with the tenants whose repository is usable. Unlike the per-physical-tenant backup endpoints, the cluster-admin surface performs no fine-grained authorization, so a missing `BACKUP` permission is never the reason.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. At least one targeted physical tenant already holds a backup with this id, or already has another backup running. The check that precedes the fan-out normally rejects the request before anything is scheduled; a tenant that takes the id in between rejects it during the fan-out instead, which can leave snapshots behind on the tenants already reached, so delete this backup id before retrying.
        errors.InternalServerErrorError: If the response status code is 500. The backup could not be scheduled on every targeted physical tenant, because one of them hit an internal error. The check that precedes the fan-out rejects the request before anything is scheduled, but a failure during the fan-out itself can leave snapshots behind on the tenants already reached, so delete this backup id before retrying.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterTakeHistoryBackupResponse"""
    response = sync_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="take_history_backup_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterTakeHistoryBackupResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[ClusterTakeHistoryBackupResponse | ProblemDetail]:
    """Take a history backup on one or every physical tenant

     Triggers a history backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. Every targeted tenant uses the same caller-supplied `backupId`, but the backups
    are independent: they are neither coordinated nor rolled back together.

    The request is all-or-nothing: the `backupId` is checked on every targeted tenant before any
    snapshot is scheduled, so a tenant that already holds this id, or that cannot be reached, fails the
    whole request and no backup is started anywhere. There is no aggregated cluster-level state in the
    response.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `POST /v2/backups/history` to act as a
    single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterTakeHistoryBackupResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, physical_tenant_id=physical_tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TakeHistoryBackupRequest,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> ClusterTakeHistoryBackupResponse:
    """Take a history backup on one or every physical tenant

     Triggers a history backup on every physical tenant of the cluster, or on the one named by
    `physicalTenantId`. Every targeted tenant uses the same caller-supplied `backupId`, but the backups
    are independent: they are neither coordinated nor rolled back together.

    The request is all-or-nothing: the `backupId` is checked on every targeted tenant before any
    snapshot is scheduled, so a tenant that already holds this id, or that cannot be reached, fails the
    whole request and no backup is started anywhere. There is no aggregated cluster-level state in the
    response.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `POST /v2/backups/history` to act as a
    single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups, or a targeted physical tenant's snapshot repository is absent from the store — configured under a name the store does not have, or not configured at all. Both are deployment faults the caller cannot correct by changing its request; narrow the request with `physicalTenantId` to work with the tenants whose repository is usable. Unlike the per-physical-tenant backup endpoints, the cluster-admin surface performs no fine-grained authorization, so a missing `BACKUP` permission is never the reason.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. At least one targeted physical tenant already holds a backup with this id, or already has another backup running. The check that precedes the fan-out normally rejects the request before anything is scheduled; a tenant that takes the id in between rejects it during the fan-out instead, which can leave snapshots behind on the tenants already reached, so delete this backup id before retrying.
        errors.InternalServerErrorError: If the response status code is 500. The backup could not be scheduled on every targeted physical tenant, because one of them hit an internal error. The check that precedes the fan-out rejects the request before anything is scheduled, but a failure during the fan-out itself can leave snapshots behind on the tenants already reached, so delete this backup id before retrying.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterTakeHistoryBackupResponse"""
    response = await asyncio_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="take_history_backup_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterTakeHistoryBackupResponse, response.parsed)
