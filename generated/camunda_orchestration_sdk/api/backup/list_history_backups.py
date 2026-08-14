from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.history_backup_info import HistoryBackupInfo
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, prefix: str | Unset = UNSET, verbose: bool | Unset = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params["prefix"] = prefix
    params["verbose"] = verbose
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/backups/history",
        "params": params,
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[HistoryBackupInfo] | None:
    if response.status_code == 200:
        response_200: list[HistoryBackupInfo] = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = HistoryBackupInfo.from_dict(response_200_item_data)
            response_200.append(response_200_item)
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
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
) -> Response[ProblemDetail | list[HistoryBackupInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
) -> Response[ProblemDetail | list[HistoryBackupInfo]]:
    """List history backups

     Returns a list of all available history backups of the physical tenant, with their state
    and additional info, most recent first by snapshot start time.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.
        verbose (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[HistoryBackupInfo]]
    """
    kwargs = _get_kwargs(prefix=prefix, verbose=verbose)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]:
    """List history backups

     Returns a list of all available history backups of the physical tenant, with their state
    and additional info, most recent first by snapshot start time.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.
        verbose (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = sync_detailed(client=client, prefix=prefix, verbose=verbose)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="list_history_backups"
        )
    assert response.parsed is not None
    return cast(list[Any], response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
) -> Response[ProblemDetail | list[HistoryBackupInfo]]:
    """List history backups

     Returns a list of all available history backups of the physical tenant, with their state
    and additional info, most recent first by snapshot start time.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.
        verbose (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[HistoryBackupInfo]]
    """
    kwargs = _get_kwargs(prefix=prefix, verbose=verbose)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    verbose: bool | Unset = UNSET,
    **kwargs: Any,
) -> list[Any]:
    """List history backups

     Returns a list of all available history backups of the physical tenant, with their state
    and additional info, most recent first by snapshot start time.

    Only available on clusters whose secondary storage is Elasticsearch or OpenSearch.

    Args:
        prefix (str | Unset): A prefix of a backup id, followed by a single '*' as a wildcard,
            matching any backup id
            starting with the given prefix.
             Example: 17567*.
        verbose (bool | Unset):

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. The request is forbidden, either because the authenticated caller lacks the required `BACKUP` permission, or because the cluster's secondary storage is neither Elasticsearch nor OpenSearch and therefore cannot serve history backups. The problem detail says which of the two applies.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = await asyncio_detailed(client=client, prefix=prefix, verbose=verbose)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="list_history_backups",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="list_history_backups"
        )
    assert response.parsed is not None
    return cast(list[Any], response.parsed)
