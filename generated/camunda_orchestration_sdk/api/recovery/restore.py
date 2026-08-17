from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_restore_response import ClusterRestoreResponse
from ...models.problem_detail import ProblemDetail
from ...models.restore_request import RestoreRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["dryRun"] = dry_run
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/restore", "params": params}
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
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
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
    *, client: AuthenticatedClient, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]:
    """Restore from a backup

     Restores the cluster from a backup. The restore is described either by a single backup ID or by a
    time range (`from`/`to`) that selects the backups to restore. This endpoint is only accessible while
    the cluster is in recovery mode; requests are rejected otherwise. The request is validated and
    acknowledged, but the restore itself is performed asynchronously.

    Args:
        dry_run (bool | Unset):
        body (RestoreRequest): Describes a restore request. Provide either a list of backup IDs or
            a time range (`from`/`to`) that selects the backups to restore; the two are mutually
            exclusive.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterRestoreResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, dry_run=dry_run)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RestoreRequest,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse:
    """Restore from a backup

     Restores the cluster from a backup. The restore is described either by a single backup ID or by a
    time range (`from`/`to`) that selects the backups to restore. This endpoint is only accessible while
    the cluster is in recovery mode; requests are rejected otherwise. The request is validated and
    acknowledged, but the restore itself is performed asynchronously.

    Args:
        dry_run (bool | Unset):
        body (RestoreRequest): Describes a restore request. Provide either a list of backup IDs or
            a time range (`from`/`to`) that selects the backups to restore; the two are mutually
            exclusive.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.ConflictError: If the response status code is 409. The cluster is not in recovery mode, so the restore cannot be accepted.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRestoreResponse"""
    response = sync_detailed(client=client, body=body, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="restore",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="restore"
        )
    assert response.parsed is not None
    return cast(ClusterRestoreResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: RestoreRequest, dry_run: bool | Unset = UNSET
) -> Response[Any | ClusterRestoreResponse | ProblemDetail]:
    """Restore from a backup

     Restores the cluster from a backup. The restore is described either by a single backup ID or by a
    time range (`from`/`to`) that selects the backups to restore. This endpoint is only accessible while
    the cluster is in recovery mode; requests are rejected otherwise. The request is validated and
    acknowledged, but the restore itself is performed asynchronously.

    Args:
        dry_run (bool | Unset):
        body (RestoreRequest): Describes a restore request. Provide either a list of backup IDs or
            a time range (`from`/`to`) that selects the backups to restore; the two are mutually
            exclusive.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ClusterRestoreResponse | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, dry_run=dry_run)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RestoreRequest,
    dry_run: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterRestoreResponse:
    """Restore from a backup

     Restores the cluster from a backup. The restore is described either by a single backup ID or by a
    time range (`from`/`to`) that selects the backups to restore. This endpoint is only accessible while
    the cluster is in recovery mode; requests are rejected otherwise. The request is validated and
    acknowledged, but the restore itself is performed asynchronously.

    Args:
        dry_run (bool | Unset):
        body (RestoreRequest): Describes a restore request. Provide either a list of backup IDs or
            a time range (`from`/`to`) that selects the backups to restore; the two are mutually
            exclusive.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.ConflictError: If the response status code is 409. The cluster is not in recovery mode, so the restore cannot be accepted.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterRestoreResponse"""
    response = await asyncio_detailed(client=client, body=body, dry_run=dry_run)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
                operation_id="restore",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="restore",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="restore"
        )
    assert response.parsed is not None
    return cast(ClusterRestoreResponse, response.parsed)
