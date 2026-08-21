from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    backup_id: int, *, physical_tenant_id: str | Unset = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params["physicalTenantId"] = physical_tenant_id
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/cluster/v2/backups/history/{backup_id}".format(
            backup_id=quote(str(backup_id), safe="")
        ),
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Delete a history backup across physical tenants

     Deletes the history backup with the given id from every physical tenant of the cluster, or from the
    one named by `physicalTenantId`. A tenant that does not hold the backup has already reached the
    requested end state, so it counts as deleted rather than as a failure.

    The request is all-or-nothing: a physical tenant the backup cannot be deleted from fails the whole
    request, and the deletions that already succeeded on other tenants are not undone. Narrow the
    request with `physicalTenantId` to delete from the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `DELETE /v2/backups/history/{backupId}`
    to act as a single physical tenant.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(backup_id=backup_id, physical_tenant_id=physical_tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Delete a history backup across physical tenants

     Deletes the history backup with the given id from every physical tenant of the cluster, or from the
    one named by `physicalTenantId`. A tenant that does not hold the backup has already reached the
    requested end state, so it counts as deleted rather than as a failure.

    The request is all-or-nothing: a physical tenant the backup cannot be deleted from fails the whole
    request, and the deletions that already succeeded on other tenants are not undone. Narrow the
    request with `physicalTenantId` to delete from the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `DELETE /v2/backups/history/{backupId}`
    to act as a single physical tenant.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The cluster's secondary storage cannot serve history backups, or a targeted physical tenant's snapshot repository is absent from the store. Unlike the per-physical-tenant backup endpoints, the cluster-admin surface performs no fine-grained authorization, so a missing `BACKUP` permission is never the reason. Deletion fans out with no preceding check, so an absent repository is found only once that tenant is reached, by which time the backup may already be deleted from the others; those deletions are not undone. Narrow the request with `physicalTenantId` to work with the tenants whose repository is usable.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster, or every targeted physical tenant was reached and none of them holds a backup with the given id.
        errors.InternalServerErrorError: If the response status code is 500. The backup could not be deleted from every targeted physical tenant, because one of them hit an internal error, so it may still exist on some of them. The deletions that already succeeded are not undone, so a retry has only the remaining tenants left to reach.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        backup_id=backup_id, client=client, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="delete_history_backup_as_cluster_admin",
        )
    return None


async def asyncio_detailed(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Delete a history backup across physical tenants

     Deletes the history backup with the given id from every physical tenant of the cluster, or from the
    one named by `physicalTenantId`. A tenant that does not hold the backup has already reached the
    requested end state, so it counts as deleted rather than as a failure.

    The request is all-or-nothing: a physical tenant the backup cannot be deleted from fails the whole
    request, and the deletions that already succeeded on other tenants are not undone. Narrow the
    request with `physicalTenantId` to delete from the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `DELETE /v2/backups/history/{backupId}`
    to act as a single physical tenant.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(backup_id=backup_id, physical_tenant_id=physical_tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    backup_id: int,
    *,
    client: AuthenticatedClient,
    physical_tenant_id: str | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Delete a history backup across physical tenants

     Deletes the history backup with the given id from every physical tenant of the cluster, or from the
    one named by `physicalTenantId`. A tenant that does not hold the backup has already reached the
    requested end state, so it counts as deleted rather than as a failure.

    The request is all-or-nothing: a physical tenant the backup cannot be deleted from fails the whole
    request, and the deletions that already succeeded on other tenants are not undone. Narrow the
    request with `physicalTenantId` to delete from the tenants that can still be reached.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here. Only available on clusters
    whose secondary storage is Elasticsearch or OpenSearch. Use `DELETE /v2/backups/history/{backupId}`
    to act as a single physical tenant.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.
        physical_tenant_id (str | Unset):  Example: default.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The cluster's secondary storage cannot serve history backups, or a targeted physical tenant's snapshot repository is absent from the store. Unlike the per-physical-tenant backup endpoints, the cluster-admin surface performs no fine-grained authorization, so a missing `BACKUP` permission is never the reason. Deletion fans out with no preceding check, so an absent repository is found only once that tenant is reached, by which time the backup may already be deleted from the others; those deletions are not undone. Narrow the request with `physicalTenantId` to work with the tenants whose repository is usable.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster, or every targeted physical tenant was reached and none of them holds a backup with the given id.
        errors.InternalServerErrorError: If the response status code is 500. The backup could not be deleted from every targeted physical tenant, because one of them hit an internal error, so it may still exist on some of them. The deletions that already succeeded are not undone, so a retry has only the remaining tenants left to reach.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        backup_id=backup_id, client=client, physical_tenant_id=physical_tenant_id
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="delete_history_backup_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="delete_history_backup_as_cluster_admin",
        )
    return None
