from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.tenant_result import TenantResult
from ...types import Response


def _get_kwargs(tenant_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenants/{tenant_id}".format(tenant_id=quote(str(tenant_id), safe="")),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantResult | None:
    if response.status_code == 200:
        response_200 = TenantResult.from_dict(response.json())
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
) -> Response[ProblemDetail | TenantResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | TenantResult]:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantResult]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> TenantResult:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
        errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantResult"""
    response = sync_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetTenantUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantResult, response.parsed)


async def asyncio_detailed(
    tenant_id: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | TenantResult]:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantResult]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> TenantResult:
    """Get tenant

     Retrieves a single tenant by tenant ID.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.

    Raises:
        errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
        errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantResult"""
    response = await asyncio_detailed(tenant_id=tenant_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetTenantUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantResult, response.parsed)
