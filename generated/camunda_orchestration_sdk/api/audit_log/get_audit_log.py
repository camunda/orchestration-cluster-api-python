from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_result import AuditLogResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(audit_log_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/audit-logs/{audit_log_key}".format(
            audit_log_key=quote(str(audit_log_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuditLogResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = AuditLogResult.from_dict(response.json())
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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuditLogResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    audit_log_key: str, *, client: AuthenticatedClient | Client
) -> Response[AuditLogResult | ProblemDetail]:
    """Get audit log

     Get an audit log entry by auditLogKey.

    Args:
        audit_log_key (str): System-generated key for an audit log entry. Example:
            22517998136843567.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogResult | ProblemDetail]
    """
    kwargs = _get_kwargs(audit_log_key=audit_log_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    audit_log_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> AuditLogResult:
    """Get audit log

     Get an audit log entry by auditLogKey.

    Args:
        audit_log_key (str): System-generated key for an audit log entry. Example:
            22517998136843567.

    Raises:
        errors.GetAuditLogUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuditLogForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuditLogNotFound: If the response status code is 404. The audit log with the given key was not found.
        errors.GetAuditLogInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuditLogResult"""
    response = sync_detailed(audit_log_key=audit_log_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuditLogUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuditLogForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetAuditLogNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuditLogInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuditLogResult, response.parsed)


async def asyncio_detailed(
    audit_log_key: str, *, client: AuthenticatedClient | Client
) -> Response[AuditLogResult | ProblemDetail]:
    """Get audit log

     Get an audit log entry by auditLogKey.

    Args:
        audit_log_key (str): System-generated key for an audit log entry. Example:
            22517998136843567.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogResult | ProblemDetail]
    """
    kwargs = _get_kwargs(audit_log_key=audit_log_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    audit_log_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> AuditLogResult:
    """Get audit log

     Get an audit log entry by auditLogKey.

    Args:
        audit_log_key (str): System-generated key for an audit log entry. Example:
            22517998136843567.

    Raises:
        errors.GetAuditLogUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetAuditLogForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetAuditLogNotFound: If the response status code is 404. The audit log with the given key was not found.
        errors.GetAuditLogInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AuditLogResult"""
    response = await asyncio_detailed(audit_log_key=audit_log_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetAuditLogUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetAuditLogForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetAuditLogNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetAuditLogInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(AuditLogResult, response.parsed)
