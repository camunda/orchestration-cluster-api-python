from http import HTTPStatus
from typing import Any
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.role_search_query_request import RoleSearchQueryRequest
from ...models.search_query_response import SearchQueryResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tenant_id: str, *, body: RoleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tenants/{tenant_id}/roles/search".format(
            tenant_id=quote(str(tenant_id), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SearchQueryResponse | None:
    if response.status_code == 200:
        response_200 = SearchQueryResponse.from_dict(response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SearchQueryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[SearchQueryResponse]:
    """Search roles for tenant

     Retrieves a filtered and sorted list of roles for a specified tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (RoleSearchQueryRequest | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchQueryResponse]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse:
    """Search roles for tenant

     Retrieves a filtered and sorted list of roles for a specified tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (RoleSearchQueryRequest | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchQueryResponse"""
    response = sync_detailed(tenant_id=tenant_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return response.parsed


async def asyncio_detailed(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
) -> Response[SearchQueryResponse]:
    """Search roles for tenant

     Retrieves a filtered and sorted list of roles for a specified tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (RoleSearchQueryRequest | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchQueryResponse]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: RoleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse:
    """Search roles for tenant

     Retrieves a filtered and sorted list of roles for a specified tenant.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        body (RoleSearchQueryRequest | Unset): Role search request.

    Raises:
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchQueryResponse"""
    response = await asyncio_detailed(tenant_id=tenant_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return response.parsed
