from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_cluster_mode_mode import ChangeClusterModeMode
from ...models.cluster_mode_change_response import ClusterModeChangeResponse
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, mode: ChangeClusterModeMode, dry_run: bool | Unset = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    json_mode = mode.value
    params["mode"] = json_mode
    params["dryRun"] = dry_run
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {"method": "patch", "url": "/mode", "params": params}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterModeChangeResponse | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClusterModeChangeResponse.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterModeChangeResponse | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterModeChangeResponse | ProblemDetail]:
    """Change cluster mode

     Transitions the cluster between processing and recovery mode. This is a non-blocking operation: the
    request is acknowledged once the change has been accepted, before the transition itself has
    completed. Entering recovery mode deactivates all partitions so that only a restricted set of read-
    only operations remains available; exiting recovery mode returns the cluster to normal processing.
    Returns the planned cluster change so its progress can be monitored via the topology.

    Args:
        mode (ChangeClusterModeMode):
        dry_run (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterModeChangeResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(mode=mode, dry_run=dry_run)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse:
    """Change cluster mode

     Transitions the cluster between processing and recovery mode. This is a non-blocking operation: the
    request is acknowledged once the change has been accepted, before the transition itself has
    completed. Entering recovery mode deactivates all partitions so that only a restricted set of read-
    only operations remains available; exiting recovery mode returns the cluster to normal processing.
    Returns the planned cluster change so its progress can be monitored via the topology.

    Args:
        mode (ChangeClusterModeMode):
        dry_run (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterModeChangeResponse"""
    response = sync_detailed(client=client, mode=mode, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="change_cluster_mode"
        )
    assert response.parsed is not None
    return cast(ClusterModeChangeResponse, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
) -> Response[ClusterModeChangeResponse | ProblemDetail]:
    """Change cluster mode

     Transitions the cluster between processing and recovery mode. This is a non-blocking operation: the
    request is acknowledged once the change has been accepted, before the transition itself has
    completed. Entering recovery mode deactivates all partitions so that only a restricted set of read-
    only operations remains available; exiting recovery mode returns the cluster to normal processing.
    Returns the planned cluster change so its progress can be monitored via the topology.

    Args:
        mode (ChangeClusterModeMode):
        dry_run (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterModeChangeResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(mode=mode, dry_run=dry_run)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    mode: ChangeClusterModeMode,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterModeChangeResponse:
    """Change cluster mode

     Transitions the cluster between processing and recovery mode. This is a non-blocking operation: the
    request is acknowledged once the change has been accepted, before the transition itself has
    completed. Entering recovery mode deactivates all partitions so that only a restricted set of read-
    only operations remains available; exiting recovery mode returns the cluster to normal processing.
    Returns the planned cluster change so its progress can be monitored via the topology.

    Args:
        mode (ChangeClusterModeMode):
        dry_run (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterModeChangeResponse"""
    response = await asyncio_detailed(client=client, mode=mode, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="change_cluster_mode",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="change_cluster_mode"
        )
    assert response.parsed is not None
    return cast(ClusterModeChangeResponse, response.parsed)
