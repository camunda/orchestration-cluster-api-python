from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.take_history_backup_request import TakeHistoryBackupRequest
from ...models.take_history_backup_response import TakeHistoryBackupResponse
from ...types import Response


def _get_kwargs(*, body: TakeHistoryBackupRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/backups/history"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TakeHistoryBackupResponse | None:
    if response.status_code == 202:
        response_202 = TakeHistoryBackupResponse.from_dict(response.json())
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
) -> Response[ProblemDetail | TakeHistoryBackupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest
) -> Response[ProblemDetail | TakeHistoryBackupResponse]:
    """Take a history backup

     Triggers a backup of the physical tenant's history, by scheduling a snapshot of every
    secondary storage index it owns.

    Unlike runtime backups, history backups have no generated-id mode: `backupId` is always
    required.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TakeHistoryBackupResponse]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest, **kwargs: Any
) -> TakeHistoryBackupResponse:
    """Take a history backup

     Triggers a backup of the physical tenant's history, by scheduling a snapshot of every
    secondary storage index it owns.

    Unlike runtime backups, history backups have no generated-id mode: `backupId` is always
    required.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.ConflictError: If the response status code is 409. A backup with the given id already exists, or another backup is already running. The "already running" check is best-effort and node-local: it only observes backups started by the gateway that serves the request. Two concurrent requests reaching different gateways are narrowed by the duplicate-id check alone.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TakeHistoryBackupResponse"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="take_history_backup"
        )
    assert response.parsed is not None
    return cast(TakeHistoryBackupResponse, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest
) -> Response[ProblemDetail | TakeHistoryBackupResponse]:
    """Take a history backup

     Triggers a backup of the physical tenant's history, by scheduling a snapshot of every
    secondary storage index it owns.

    Unlike runtime backups, history backups have no generated-id mode: `backupId` is always
    required.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TakeHistoryBackupResponse]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: TakeHistoryBackupRequest, **kwargs: Any
) -> TakeHistoryBackupResponse:
    """Take a history backup

     Triggers a backup of the physical tenant's history, by scheduling a snapshot of every
    secondary storage index it owns.

    Unlike runtime backups, history backups have no generated-id mode: `backupId` is always
    required.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        body (TakeHistoryBackupRequest): Request body for taking a history backup.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.ConflictError: If the response status code is 409. A backup with the given id already exists, or another backup is already running. The "already running" check is best-effort and node-local: it only observes backups started by the gateway that serves the request. Two concurrent requests reaching different gateways are narrowed by the duplicate-id check alone.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TakeHistoryBackupResponse"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 409:
            raise errors.ConflictError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="take_history_backup",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="take_history_backup"
        )
    assert response.parsed is not None
    return cast(TakeHistoryBackupResponse, response.parsed)
