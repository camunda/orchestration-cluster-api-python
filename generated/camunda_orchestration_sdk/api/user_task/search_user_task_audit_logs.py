from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_search_query_result import AuditLogSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...models.user_task_audit_log_search_query_request import (
    UserTaskAuditLogSearchQueryRequest,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_task_key: str, *, body: UserTaskAuditLogSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user-tasks/{user_task_key}/audit-logs/search".format(
            user_task_key=quote(str(user_task_key), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuditLogSearchQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = AuditLogSearchQueryResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuditLogSearchQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskAuditLogSearchQueryRequest | Unset = UNSET,
) -> Response[AuditLogSearchQueryResult | ProblemDetail]:
    """Search user task audit logs

     Search for user task audit logs based on given criteria.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskAuditLogSearchQueryRequest | Unset): User task search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskAuditLogSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> AuditLogSearchQueryResult:
    """Search user task audit logs

     Search for user task audit logs based on given criteria.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskAuditLogSearchQueryRequest | Unset): User task search query request.

    Raises:
        errors.SearchUserTaskAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchUserTaskAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuditLogSearchQueryResult"""
    response = sync_detailed(user_task_key=user_task_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchUserTaskAuditLogsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchUserTaskAuditLogsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuditLogSearchQueryResult, response.parsed)


async def asyncio_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskAuditLogSearchQueryRequest | Unset = UNSET,
) -> Response[AuditLogSearchQueryResult | ProblemDetail]:
    """Search user task audit logs

     Search for user task audit logs based on given criteria.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskAuditLogSearchQueryRequest | Unset): User task search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(user_task_key=user_task_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: UserTaskAuditLogSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> AuditLogSearchQueryResult:
    """Search user task audit logs

     Search for user task audit logs based on given criteria.

    Args:
        user_task_key (str): System-generated key for a user task.
        body (UserTaskAuditLogSearchQueryRequest | Unset): User task search query request.

    Raises:
        errors.SearchUserTaskAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchUserTaskAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuditLogSearchQueryResult"""
    response = await asyncio_detailed(
        user_task_key=user_task_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchUserTaskAuditLogsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchUserTaskAuditLogsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuditLogSearchQueryResult, response.parsed)
