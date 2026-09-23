from http import HTTPStatus
from typing import Any
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_upgrade_status_response import ClusterUpgradeStatusResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/cluster/v2/status/upgrade"}
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterUpgradeStatusResponse | None:
    if response.status_code == 200:
        response_200 = ClusterUpgradeStatusResponse.from_dict(response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterUpgradeStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterUpgradeStatusResponse]:
    """Get the upgrade-readiness status of the whole cluster

     Reports one overall upgrade-readiness status for the whole cluster, folded over every physical
    tenant and condition. `MIGRATED` only once every known condition has migrated for every known
    physical tenant; `MIGRATION_IN_PROGRESS` when at least one is confirmed not yet migrated; `UNKNOWN`
    otherwise (including before anything has been reported yet). No per-tenant or per-condition detail
    is reported here; see the `upgradeReadiness` actuator endpoint for that.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterUpgradeStatusResponse]
    """
    kwargs = _get_kwargs()
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterUpgradeStatusResponse:
    """Get the upgrade-readiness status of the whole cluster

     Reports one overall upgrade-readiness status for the whole cluster, folded over every physical
    tenant and condition. `MIGRATED` only once every known condition has migrated for every known
    physical tenant; `MIGRATION_IN_PROGRESS` when at least one is confirmed not yet migrated; `UNKNOWN`
    otherwise (including before anything has been reported yet). No per-tenant or per-condition detail
    is reported here; see the `upgradeReadiness` actuator endpoint for that.

    Raises:
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterUpgradeStatusResponse"""
    response = sync_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_cluster_upgrade_status",
        )
    assert response.parsed is not None
    return response.parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client
) -> Response[ClusterUpgradeStatusResponse]:
    """Get the upgrade-readiness status of the whole cluster

     Reports one overall upgrade-readiness status for the whole cluster, folded over every physical
    tenant and condition. `MIGRATED` only once every known condition has migrated for every known
    physical tenant; `MIGRATION_IN_PROGRESS` when at least one is confirmed not yet migrated; `UNKNOWN`
    otherwise (including before anything has been reported yet). No per-tenant or per-condition detail
    is reported here; see the `upgradeReadiness` actuator endpoint for that.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterUpgradeStatusResponse]
    """
    kwargs = _get_kwargs()
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterUpgradeStatusResponse:
    """Get the upgrade-readiness status of the whole cluster

     Reports one overall upgrade-readiness status for the whole cluster, folded over every physical
    tenant and condition. `MIGRATED` only once every known condition has migrated for every known
    physical tenant; `MIGRATION_IN_PROGRESS` when at least one is confirmed not yet migrated; `UNKNOWN`
    otherwise (including before anything has been reported yet). No per-tenant or per-condition detail
    is reported here; see the `upgradeReadiness` actuator endpoint for that.

    Raises:
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterUpgradeStatusResponse"""
    response = await asyncio_detailed(client=client)
    if response.status_code < 200 or response.status_code >= 300:
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="get_cluster_upgrade_status",
        )
    assert response.parsed is not None
    return response.parsed
