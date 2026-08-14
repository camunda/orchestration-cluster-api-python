from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_mode_change_response import ClusterModeChangeResponse
from ...models.mode import Mode
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    json_mode = mode.value
    params["mode"] = json_mode
    params["physicalTenantId"] = physical_tenant_id
    params["dryRun"] = dry_run
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/cluster/v2/mode",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ClusterModeChangeResponse | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClusterModeChangeResponse.from_dict(response.json())
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
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]:
    """Change the cluster mode of one or every physical tenant

     Transitions physical tenants between processing and recovery mode.

    If the `physicalTenantId` parameter is not provided, all available physical tenants are transitioned
    individually.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        mode (Mode): The operating mode of a cluster's partitions.
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterModeChangeResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(
        mode=mode, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse:
    """Change the cluster mode of one or every physical tenant

     Transitions physical tenants between processing and recovery mode.

    If the `physicalTenantId` parameter is not provided, all available physical tenants are transitioned
    individually.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        mode (Mode): The operating mode of a cluster's partitions.
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. The mode change conflicts with the cluster state, for example because another configuration change is in progress.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterModeChangeResponse"""
    response = sync_detailed(
        client=client, mode=mode, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="change_cluster_mode_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterModeChangeResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
) -> Response[Any | ClusterModeChangeResponse | ProblemDetail]:
    """Change the cluster mode of one or every physical tenant

     Transitions physical tenants between processing and recovery mode.

    If the `physicalTenantId` parameter is not provided, all available physical tenants are transitioned
    individually.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        mode (Mode): The operating mode of a cluster's partitions.
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterModeChangeResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(
        mode=mode, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    mode: Mode,
    physical_tenant_id: str | Unset = UNSET,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse:
    """Change the cluster mode of one or every physical tenant

     Transitions physical tenants between processing and recovery mode.

    If the `physicalTenantId` parameter is not provided, all available physical tenants are transitioned
    individually.

    Requires the cluster-admin security chain. Although this operation lists `bearerAuth` / `basicAuth`
    like the rest of the Orchestration Cluster API, it does not accept an Orchestration Cluster user's
    credentials — only the separate cluster-admin credentials are valid here.

    Args:
        mode (Mode): The operating mode of a cluster's partitions.
        physical_tenant_id (str | Unset):  Example: default.
        dry_run (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.NotFoundError: If the response status code is 404. The requested `physicalTenantId` does not exist in this cluster.
        errors.ConflictError: If the response status code is 409. The mode change conflicts with the cluster state, for example because another configuration change is in progress.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterModeChangeResponse"""
    response = await asyncio_detailed(
        client=client, mode=mode, physical_tenant_id=physical_tenant_id, dry_run=dry_run
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode_as_cluster_admin",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="change_cluster_mode_as_cluster_admin",
        )
    assert response.parsed is not None
    return cast(ClusterModeChangeResponse, response.parsed)
