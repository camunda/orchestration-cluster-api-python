from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.tenant_create_request import TenantCreateRequest
from ...models.tenant_create_result import TenantCreateResult
from ...types import Response


def _get_kwargs(*, body: TenantCreateRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/tenants"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | TenantCreateResult | None:
    if response.status_code == 201:
        response_201 = TenantCreateResult.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = cast(Any, None)
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
) -> Response[Any | ProblemDetail | TenantCreateResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: TenantCreateRequest
) -> Response[Any | ProblemDetail | TenantCreateResult]:
    """Create tenant

     Creates a new tenant.

    Args:
        body (TenantCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail | TenantCreateResult]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, body: TenantCreateRequest, **kwargs: Any
) -> TenantCreateResult:
    """Create tenant

     Creates a new tenant.

    Args:
        body (TenantCreateRequest):

    Raises:
        errors.CreateTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateTenantNotFound: If the response status code is 404. Not found. The resource was not found.
        errors.CreateTenantConflict: If the response status code is 409. Tenant with this id already exists.
        errors.CreateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantCreateResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CreateTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateTenantConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        if response.status_code == 500:
            raise errors.CreateTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantCreateResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: TenantCreateRequest
) -> Response[Any | ProblemDetail | TenantCreateResult]:
    """Create tenant

     Creates a new tenant.

    Args:
        body (TenantCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail | TenantCreateResult]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, body: TenantCreateRequest, **kwargs: Any
) -> TenantCreateResult:
    """Create tenant

     Creates a new tenant.

    Args:
        body (TenantCreateRequest):

    Raises:
        errors.CreateTenantBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.CreateTenantNotFound: If the response status code is 404. Not found. The resource was not found.
        errors.CreateTenantConflict: If the response status code is 409. Tenant with this id already exists.
        errors.CreateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        TenantCreateResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateTenantBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.CreateTenantForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CreateTenantNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CreateTenantConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=response.parsed,
            )
        if response.status_code == 500:
            raise errors.CreateTenantInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateTenantServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(TenantCreateResult, response.parsed)
