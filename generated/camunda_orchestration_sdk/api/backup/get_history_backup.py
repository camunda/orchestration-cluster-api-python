from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.history_backup_info import HistoryBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(backup_id: int) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/backups/history/{backup_id}".format(
            backup_id=quote(str(backup_id), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HistoryBackupInfo | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = HistoryBackupInfo.from_dict(response.json())
        return response_200
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
) -> Response[HistoryBackupInfo | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[HistoryBackupInfo | ProblemDetail]:
    """Get history backup

     Returns detailed status of the history backup with the given id.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HistoryBackupInfo | ProblemDetail]
    """
    kwargs = _get_kwargs(backup_id=backup_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> HistoryBackupInfo:
    """Get history backup

     Returns detailed status of the history backup with the given id.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.NotFoundError: If the response status code is 404. A backup with the given id does not exist.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        HistoryBackupInfo"""
    response = sync_detailed(backup_id=backup_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_history_backup"
        )
    assert response.parsed is not None
    return cast(HistoryBackupInfo, response.parsed)


async def asyncio_detailed(
    backup_id: int, *, client: AuthenticatedClient
) -> Response[HistoryBackupInfo | ProblemDetail]:
    """Get history backup

     Returns detailed status of the history backup with the given id.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HistoryBackupInfo | ProblemDetail]
    """
    kwargs = _get_kwargs(backup_id=backup_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    backup_id: int, *, client: AuthenticatedClient, **kwargs: Any
) -> HistoryBackupInfo:
    """Get history backup

     Returns detailed status of the history backup with the given id.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        backup_id (int): The id of the backup. Must be a positive numerical value. As backups are
            logically
            ordered by their ids (ascending), each successive backup must use a higher id than the
            previous one.
             Example: 1.

    Raises:
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.NotFoundError: If the response status code is 404. A backup with the given id does not exist.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        HistoryBackupInfo"""
    response = await asyncio_detailed(backup_id=backup_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_history_backup",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_history_backup"
        )
    assert response.parsed is not None
    return cast(HistoryBackupInfo, response.parsed)
