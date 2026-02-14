from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_search_query_request import AuditLogSearchQueryRequest
from ...models.problem_detail import ProblemDetail
from ...models.search_audit_logs_response_200 import SearchAuditLogsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: AuditLogSearchQueryRequest | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/audit-logs/search"}
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | SearchAuditLogsResponse200 | None:
    if response.status_code == 200:
        response_200 = SearchAuditLogsResponse200.from_dict(response.json())
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
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail | SearchAuditLogsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuditLogSearchQueryRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail | SearchAuditLogsResponse200]:
    """Search audit logs

     Search for audit logs based on given criteria.

    Args:
        body (AuditLogSearchQueryRequest | Unset): Audit log search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail | SearchAuditLogsResponse200]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AuditLogSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchAuditLogsResponse200:
    """Search audit logs

     Search for audit logs based on given criteria.

    Args:
        body (AuditLogSearchQueryRequest | Unset): Audit log search request.

    Raises:
        errors.SearchAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchAuditLogsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchAuditLogsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchAuditLogsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchAuditLogsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchAuditLogsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchAuditLogsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchAuditLogsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchAuditLogsResponse200, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuditLogSearchQueryRequest | Unset = UNSET,
) -> Response[Any | ProblemDetail | SearchAuditLogsResponse200]:
    """Search audit logs

     Search for audit logs based on given criteria.

    Args:
        body (AuditLogSearchQueryRequest | Unset): Audit log search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail | SearchAuditLogsResponse200]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AuditLogSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchAuditLogsResponse200:
    """Search audit logs

     Search for audit logs based on given criteria.

    Args:
        body (AuditLogSearchQueryRequest | Unset): Audit log search request.

    Raises:
        errors.SearchAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchAuditLogsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchAuditLogsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchAuditLogsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchAuditLogsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchAuditLogsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchAuditLogsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchAuditLogsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchAuditLogsResponse200, response.parsed)
