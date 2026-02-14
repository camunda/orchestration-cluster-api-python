from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.tenant_update_request import TenantUpdateRequest
from ...models.tenant_update_result import TenantUpdateResult
from ...types import Response


def _get_kwargs(tenant_id: str, *, body: TenantUpdateRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/tenants/{tenant_id}".format(tenant_id=quote(str(tenant_id), safe="")),
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | TenantUpdateResult | None:
    if response.status_code == 200:
        response_200 = TenantUpdateResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
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
) -> Response[ProblemDetail | TenantUpdateResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str, *, client: AuthenticatedClient | Client, body: TenantUpdateRequest
) -> Response[ProblemDetail | TenantUpdateResult]:
    """Update tenant

     Updates an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (TenantUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantUpdateResult]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TenantUpdateRequest,
    **kwargs: Any,
) -> TenantUpdateResult:
    """Update tenant

     Updates an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (TenantUpdateRequest):

    Raises:
        errors.UpdateTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UpdateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UpdateTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
        errors.UpdateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UpdateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantUpdateResult"""
    response = sync_detailed(tenant_id=tenant_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UpdateTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UpdateTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UpdateTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UpdateTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantUpdateResult, response.parsed)


async def asyncio_detailed(
    tenant_id: str, *, client: AuthenticatedClient | Client, body: TenantUpdateRequest
) -> Response[ProblemDetail | TenantUpdateResult]:
    """Update tenant

     Updates an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (TenantUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | TenantUpdateResult]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TenantUpdateRequest,
    **kwargs: Any,
) -> TenantUpdateResult:
    """Update tenant

     Updates an existing tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (TenantUpdateRequest):

    Raises:
        errors.UpdateTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.UpdateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.UpdateTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
        errors.UpdateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UpdateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantUpdateResult"""
    response = await asyncio_detailed(tenant_id=tenant_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UpdateTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.UpdateTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.UpdateTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.UpdateTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.UpdateTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantUpdateResult, response.parsed)
