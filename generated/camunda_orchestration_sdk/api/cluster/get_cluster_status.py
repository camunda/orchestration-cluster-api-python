from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_status_response import ClusterStatusResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/cluster/v2/status"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterStatusResponse | None:
    if response.status_code == 200:
        response_200 = ClusterStatusResponse.from_dict(response.json())
        return response_200
    if response.status_code == 503:
        response_503 = ClusterStatusResponse.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterStatusResponse]:
    """Get the status of the whole cluster

     Checks the health status of the whole cluster, aggregated over all physical tenants. Returns
    `HEALTHY` when every physical tenant is healthy, `DOWN` when no physical tenant can process work,
    and `DEGRADED` in every other case. No per-tenant detail is reported; use `GET /cluster/v2/topology`
    for that.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterStatusResponse]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterStatusResponse:
    """Get the status of the whole cluster

     Checks the health status of the whole cluster, aggregated over all physical tenants. Returns
    `HEALTHY` when every physical tenant is healthy, `DOWN` when no physical tenant can process work,
    and `DEGRADED` in every other case. No per-tenant detail is reported; use `GET /cluster/v2/topology`
    for that.

    Raises:
        errors.ServiceUnavailableError: If the response status code is 503. The cluster is DOWN because no physical tenant can process work.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterStatusResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterStatusResponse, response.parsed),
                operation_id="get_cluster_status",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_cluster_status"
        )
    assert response.parsed is not None
    return response.parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterStatusResponse]:
    """Get the status of the whole cluster

     Checks the health status of the whole cluster, aggregated over all physical tenants. Returns
    `HEALTHY` when every physical tenant is healthy, `DOWN` when no physical tenant can process work,
    and `DEGRADED` in every other case. No per-tenant detail is reported; use `GET /cluster/v2/topology`
    for that.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterStatusResponse]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterStatusResponse:
    """Get the status of the whole cluster

     Checks the health status of the whole cluster, aggregated over all physical tenants. Returns
    `HEALTHY` when every physical tenant is healthy, `DOWN` when no physical tenant can process work,
    and `DEGRADED` in every other case. No per-tenant detail is reported; use `GET /cluster/v2/topology`
    for that.

    Raises:
        errors.ServiceUnavailableError: If the response status code is 503. The cluster is DOWN because no physical tenant can process work.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterStatusResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ClusterStatusResponse, response.parsed),
                operation_id="get_cluster_status",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_cluster_status"
        )
    assert response.parsed is not None
    return response.parsed
