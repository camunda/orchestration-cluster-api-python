from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_runtime_backup_info import ClusterRuntimeBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, physical_tenant_id: str | Unset = UNSET, prefix: str | Unset = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params["prefix"] = prefix
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cluster/v2/backups/runtime",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[ClusterRuntimeBackupInfo] | None:
    if response.status_code == 200:
        response_200: list[ClusterRuntimeBackupInfo] = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ClusterRuntimeBackupInfo.from_dict(
                response_200_item_data
            )
            response_200.append(response_200_item)
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
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
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]:
    """List runtime backups across physical tenants

     Lists the runtime backups of every physical tenant of the cluster, or of the one named by
    `physicalTenantId`, grouped by backup id. Every group reports every targeted tenant, including the
    ones holding nothing for that id, so a backup only some tenants hold aggregates to `INCOMPLETE` here
    exactly as it does when looked up directly — the state of a listed group can be trusted to say
    whether the cluster can be restored from it. A backup id that only some physical tenants hold is a
    supported outcome rather than a degraded one; tenants that generate their own backup ids never share
    one, so in that mode each backup forms its own group and the other tenants report `DOES_NOT_EXIST`
    under it.

    The request is all-or-nothing: a physical tenant whose backups cannot be read fails the whole
    request rather than silently dropping out of the listing. Narrow the request with `physicalTenantId`
    to list the backups of the tenants that can still be read.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]
    """
    kwargs = _get_kwargs(physical_tenant_id=physical_tenant_id, prefix=prefix)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]:
    """List runtime backups across physical tenants

     Lists the runtime backups of every physical tenant of the cluster, or of the one named by
    `physicalTenantId`, grouped by backup id. Every group reports every targeted tenant, including the
    ones holding nothing for that id, so a backup only some tenants hold aggregates to `INCOMPLETE` here
    exactly as it does when looked up directly — the state of a listed group can be trusted to say
    whether the cluster can be restored from it. A backup id that only some physical tenants hold is a
    supported outcome rather than a degraded one; tenants that generate their own backup ids never share
    one, so in that mode each backup forms its own group and the other tenants report `DOES_NOT_EXIST`
    under it.

    The request is all-or-nothing: a physical tenant whose backups cannot be read fails the whole
    request rather than silently dropping out of the listing. Narrow the request with `physicalTenantId`
    to list the backups of the tenants that can still be read.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = sync_detailed(
        client=client, physical_tenant_id=physical_tenant_id, prefix=prefix
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="list_runtime_backups_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(list[Any], response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
) -> Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]:
    """List runtime backups across physical tenants

     Lists the runtime backups of every physical tenant of the cluster, or of the one named by
    `physicalTenantId`, grouped by backup id. Every group reports every targeted tenant, including the
    ones holding nothing for that id, so a backup only some tenants hold aggregates to `INCOMPLETE` here
    exactly as it does when looked up directly — the state of a listed group can be trusted to say
    whether the cluster can be restored from it. A backup id that only some physical tenants hold is a
    supported outcome rather than a degraded one; tenants that generate their own backup ids never share
    one, so in that mode each backup forms its own group and the other tenants report `DOES_NOT_EXIST`
    under it.

    The request is all-or-nothing: a physical tenant whose backups cannot be read fails the whole
    request rather than silently dropping out of the listing. Narrow the request with `physicalTenantId`
    to list the backups of the tenants that can still be read.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[ClusterRuntimeBackupInfo]]
    """
    kwargs = _get_kwargs(physical_tenant_id=physical_tenant_id, prefix=prefix)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    prefix: str | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]:
    """List runtime backups across physical tenants

     Lists the runtime backups of every physical tenant of the cluster, or of the one named by
    `physicalTenantId`, grouped by backup id. Every group reports every targeted tenant, including the
    ones holding nothing for that id, so a backup only some tenants hold aggregates to `INCOMPLETE` here
    exactly as it does when looked up directly — the state of a listed group can be trusted to say
    whether the cluster can be restored from it. A backup id that only some physical tenants hold is a
    supported outcome rather than a degraded one; tenants that generate their own backup ids never share
    one, so in that mode each backup forms its own group and the other tenants report `DOES_NOT_EXIST`
    under it.

    The request is all-or-nothing: a physical tenant whose backups cannot be read fails the whole
    request rather than silently dropping out of the listing. Narrow the request with `physicalTenantId`
    to list the backups of the tenants that can still be read.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Use `GET
    /v2/backups/runtime` to act as a single physical tenant.

    Args:
        physical_tenant_id (str | Unset):  Example: default.
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = await asyncio_detailed(
        client=client, physical_tenant_id=physical_tenant_id, prefix=prefix
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_runtime_backups_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="list_runtime_backups_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(list[Any], response.parsed)
