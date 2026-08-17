from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_restore_request import ClusterRestoreRequest
from ...models.cluster_restore_response import ClusterRestoreResponse
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params["dryRun"] = dry_run
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cluster/v2/restore",
        "params": params,
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ClusterRestoreResponse | ProblemDetail | None:
    if response.status_code == 202:
        response_202 = ClusterRestoreResponse.from_dict(response.json())
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
        response_409 = cast(Any, None)
        return response_409
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]:
    """Restore one or every physical tenant from a backup

     Restores physical tenants from backups. The restore is described either by a list of backup IDs or
    by a time range (`from`/`to`) that selects the backups to restore. Restores are only accepted while
    the targeted physical tenants are in recovery mode; requests are rejected otherwise. The request is
    validated and acknowledged, but the restore itself is performed asynchronously.

    If the `physicalTenantId` parameter is provided, only that physical tenant is restored and
    `overrides` must be omitted.

    If it is not provided, every physical tenant of the cluster is restored: those named in `overrides`
    with their own backup selection, all others with the selection at the top level of the request body.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):
        body (ClusterRestoreRequest): Describes a restore request issued by a cluster admin. The
            backup selection at the top level applies to every targeted physical tenant, except for
            the ones listed in `overrides`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterRestoreResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(
        body=body, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse:
    """Restore one or every physical tenant from a backup

     Restores physical tenants from backups. The restore is described either by a list of backup IDs or
    by a time range (`from`/`to`) that selects the backups to restore. Restores are only accepted while
    the targeted physical tenants are in recovery mode; requests are rejected otherwise. The request is
    validated and acknowledged, but the restore itself is performed asynchronously.

    If the `physicalTenantId` parameter is provided, only that physical tenant is restored and
    `overrides` must be omitted.

    If it is not provided, every physical tenant of the cluster is restored: those named in `overrides`
    with their own backup selection, all others with the selection at the top level of the request body.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):
        body (ClusterRestoreRequest): Describes a restore request issued by a cluster admin. The
            backup selection at the top level applies to every targeted physical tenant, except for
            the ones listed in `overrides`.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId`, or a physical tenant named in `overrides`, does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. A targeted physical tenant is not in recovery mode, so the restore cannot be accepted.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRestoreResponse"""
    response = sync_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="restore_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterRestoreResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]:
    """Restore one or every physical tenant from a backup

     Restores physical tenants from backups. The restore is described either by a list of backup IDs or
    by a time range (`from`/`to`) that selects the backups to restore. Restores are only accepted while
    the targeted physical tenants are in recovery mode; requests are rejected otherwise. The request is
    validated and acknowledged, but the restore itself is performed asynchronously.

    If the `physicalTenantId` parameter is provided, only that physical tenant is restored and
    `overrides` must be omitted.

    If it is not provided, every physical tenant of the cluster is restored: those named in `overrides`
    with their own backup selection, all others with the selection at the top level of the request body.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):
        body (ClusterRestoreRequest): Describes a restore request issued by a cluster admin. The
            backup selection at the top level applies to every targeted physical tenant, except for
            the ones listed in `overrides`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterRestoreResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(
        body=body, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ClusterRestoreRequest,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse:
    """Restore one or every physical tenant from a backup

     Restores physical tenants from backups. The restore is described either by a list of backup IDs or
    by a time range (`from`/`to`) that selects the backups to restore. Restores are only accepted while
    the targeted physical tenants are in recovery mode; requests are rejected otherwise. The request is
    validated and acknowledged, but the restore itself is performed asynchronously.

    If the `physicalTenantId` parameter is provided, only that physical tenant is restored and
    `overrides` must be omitted.

    If it is not provided, every physical tenant of the cluster is restored: those named in `overrides`
    with their own backup selection, all others with the selection at the top level of the request body.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):
        body (ClusterRestoreRequest): Describes a restore request issued by a cluster admin. The
            backup selection at the top level applies to every targeted physical tenant, except for
            the ones listed in `overrides`.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId`, or a physical tenant named in `overrides`, does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. A targeted physical tenant is not in recovery mode, so the restore cannot be accepted.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRestoreResponse"""
    response = await asyncio_detailed(
        client=client, body=body, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="restore_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="restore_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterRestoreResponse, response.parsed)
